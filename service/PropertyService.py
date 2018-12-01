from common.request_constants.HttpStatus import HttpStatus
from common.request_constants.FieldKey import FieldKey
from common.Error import Error
from common.validator.persistence.PropertyValidator import PropertyValidator

from database.ReadOnlyAccess import ReadOnlyAccess
from domain.Property import Property
from domain.Rental import Rental
from domain.Viewing import Viewing
from domain.Image import Image

from task.TaskProcessor import TaskProcessor
from task.repository.SaveNewEntityTask import SaveNewEntityTask
from task.repository.UpdateEntityTask import UpdateEntityTask
from task.repository.DeleteEntityTask import DeleteEntityTask
from task.repository.DetachForeignKeyTask import DetachForeignKeyTask
from task.file_system.SaveToFileSystemTask import SaveToFileSystemTask
from task.file_system.RemoveFromFileSystemTask import RemoveFromFileSystemTask
from task.file_system.FlushDirectoryTask import FlushDirectoryTask

'''
Validates Properties agains the persistence layer,
reads Properties from the persistence layer,
and performs operations on Properties via Tasks
'''
class PropertyService():
    def create(property):
        # Validate in persistence level
        validatorResponse = PropertyValidator.validateCreate(property)
        if FieldKey.ERROR in validatorResponse:
            return validatorResponse
        # Create and process Tasks
        processor = TaskProcessor()
        processor.add(SaveNewEntityTask(property))
        processor.process()
        # Return Result
        return {FieldKey.SUCCESS: property}

    def read(propertyId):
        # Validate in persistence level
        validatorResponse = PropertyValidator.validateRead(propertyId)
        if FieldKey.ERROR in validatorResponse:
            return validatorResponse
        # Read Entity
        property = ReadOnlyAccess.getEntityCopy(Property, propertyId)
        # Return Result
        return {FieldKey.SUCCESS: property}

    def update(ownerId, updatedProperty):
        # Validate in persistence level
        validatorResponse = PropertyValidator.validateUpdate(ownerId, updatedProperty)
        if FieldKey.ERROR in validatorResponse:
            return validatorResponse
        # Create and process Tasks
        processor = TaskProcessor()
        processor.add(UpdateEntityTask(Property, PropertyService.mergeProperties, updatedProperty))
        processor.process()
        # Return Result
        property = ReadOnlyAccess.getEntityCopy(Property, updatedProperty.id)
        return {FieldKey.SUCCESS: property}

    def delete(ownerId, propertyId):
        # Validate in persistence level
        validatorResponse = PropertyValidator.validateDelete(ownerId, propertyId)
        if FieldKey.ERROR in validatorResponse:
            return validatorResponse
        # Get return copy, before delete
        property = ReadOnlyAccess.getEntityCopy(Property, propertyId)
        # Create and process Tasks
        processor = TaskProcessor()
        processor.add(DetachForeignKeyTask(Rental, "property", propertyId))
        processor.add(DetachForeignKeyTask(Viewing, "propertyId", propertyId))
        for image in ReadOnlyAccess.getEntityListCopy(Image, {"propertyId": propertyId}):
            processor.add(RemoveFromFileSystemTask("images", ownerId, image.id, "jpg"))
            processor.add(DeleteEntityTask(Image, image.id))
        processor.add(DeleteEntityTask(Property, propertyId))
        processor.add(FlushDirectoryTask("images", []))
        processor.process()
        # Return Result
        return {FieldKey.SUCCESS: property}

    def readAll(ownerId):
        # Validate in persistence level
        validatorResponse = PropertyValidator.validateReadAll(ownerId)
        if FieldKey.ERROR in validatorResponse:
            return validatorResponse
        # Read Entities
        searchFilter = {"ownerId": ownerId}
        propertyList = ReadOnlyAccess.getEntityListCopy(Property, searchFilter)
        # Return Result
        return {FieldKey.SUCCESS: propertyList}

    def history(ownerId, start, end):
        # Validate in persistence level
        validatorResponse = AccountValidator.validateHistory(ownerId, start, end)
        if FieldKey.ERROR in validatorResponse:
            return validatorResponse

        history = []
        searchFilter = {"ownerId": ownerId}
        propertyList = ReadOnlyAccess.getEntityListCopy(Property, searchFilter)
        for property in propertyList:
            history.append(PropertyService.generateHistory(property, start, end))
        return history

    def generateHistory(property, start, end):
        searchFilter = {"property": property.id}
        rentalList = ReadOnlyAccess.getEntityListCopy(Rental, searchFilter)
        searchFilter = {"propertyId": property.id}
        viewingList = ReadOnlyAccess.getEntityListCopy(Rental, searchFilter)
        rentalList = list(filter(lambda x: Date.overlap(start, end, x.start, x.end), rentalList))
        viewingList = list(filter(lambda x: Date.bewteen(x.date, start, end), viewingList))

        stats = {
            "rental": {
                "leases_proposed": 0,
                "leases_cancelled": 0,
                "leases_accepted": 0,
                "average_lease_length": 0,
                "time_rented": 0,
                "time_vacant": 0,
                "average_rent_non_vacant": 0,
                "average_rent": 0
            },
            "viewing": {
                "count": 0,
                "frequency": 0
            }
        }

        total_accepted_lease_length_days = 0
        total_rent_days = 0
        for rental in rentalList:
            stats["rental"]["leases_proposed"] += 1
            if rental.status == RentalStatus.CONFIRMED:
                stats["rental"]["leases_accepted"] += 1
                total_accepted_lease_length_days += Date.lengthDays(Date.toDate(rental.start), Date.toDate(rental.end))
                total_rent_days += Date.lengthDays(Date.toDate(rental.start), Date.toDate(rental.end)) * int(rental.rent)
            if rental.status == RentalStatus.CANCELLED:
                stats["rental"]["leases_accepted"] += 1
                stats["rental"]["leases_cancelled"] += 1
                total_accepted_lease_length_days += Date.lengthDays(Date.toDate(rental.start), Date.toDate(rental.end))
                total_rent_days += Date.lengthDays(Date.toDate(rental.start), Date.toDate(rental.end)) * int(rental.rent)
        total_accepted_lease_length_days = total_accepted_lease_length_days if total_accepted_lease_length_days > 0 else 1
        stats["rental"]["time_rented"] = Date.roundToMonths(total_accepted_lease_length_days)
        stats["rental"]["time_vacant"] = Date.roundToMonths(Date.lengthDays(Date.toDate(start), Date.toDate(end)) - total_accepted_lease_length_days)
        stats["rental"]["average_rent_non_vacant"] = Date.roundToMonths(total_accepted_lease_length_days) * total_rent_days // total_accepted_lease_length_days
        stats["rental"]["average_rent"] = Date.roundToMonths(total_accepted_lease_length_days) * total_rent_days // Date.lengthDays(Date.toDate(start), Date.toDate(end))

        durationMonths = Date.roundToMonths(Date.lengthDays(Date.toDate(start), Date.toDate(end)))
        durationMonths = durationMonths if durationMonths > 0 else 1
        for viewing in viewingList:
            stats["viewing"]["count"] += 1
        stats["viewing"]["frequency"] = stats["viewing"]["count"] // durationMonths
        return stats

    FILTERABLE_SEARCH_CRITERIA = ["city", "province"]
    def search(criteria):
        # Read Entities
        searchFilter = {}
        for k in criteria:
            if criteria[k] is not None and k in PropertyService.FILTERABLE_SEARCH_CRITERIA:
                searchFilter[k] = criteria[k]
        propertyList = ReadOnlyAccess.getEntityListCopy(Property, searchFilter)
        if criteria["min"] is not None:
            propertyList = list(filter(lambda x: int(x.rent) >= criteria["min"], propertyList))
        if criteria["max"] is not None:
            propertyList = list(filter(lambda x: int(x.rent) <= criteria["max"], propertyList))
        # Return Result
        return {FieldKey.SUCCESS: propertyList}

    def mergeProperties(original, new):
        original.mainImageId = new.mainImageId if new.mainImageId is not None else original.mainImageId
        original.city = new.city if new.city is not None else original.city
        original.province = new.province if new.province is not None else original.province
        original.rent = new.rent if new.rent is not None else original.rent
        original.addr1 = new.addr1 if new.addr1 is not None else original.addr1
        original.addr2 = new.addr2 if new.addr2 is not None else original.addr2
        return original
