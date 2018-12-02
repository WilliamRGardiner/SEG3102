import copy

from common.converter.RentalConverter import RentalConverter
from common.request_constants.HttpStatus import HttpStatus
from common.request_constants.FieldKey import FieldKey
from common.Error import Error
from common.validator.persistence.RentalValidator import RentalValidator

from database.Repository import Repository
from database.ReadOnlyAccess import ReadOnlyAccess
from domain.Rental import Rental, RentalStatus

from task.TaskProcessor import TaskProcessor
from task.repository.SaveNewEntityTask import SaveNewEntityTask
from task.repository.UpdateEntityTask import UpdateEntityTask
from task.repository.DeleteEntityTask import DeleteEntityTask

'''
Validates Rentals agains the persistence layer,
reads Rentals from the persistence layer,
and performs operations on Rentals via Tasks
'''
class RentalService():
    def create(rental):
        # Validate in persistence level
        validatorResponse = RentalValidator.validateCreate(rental)
        if FieldKey.ERROR in validatorResponse:
            return validatorResponse
        # Create and process Tasks
        processor = TaskProcessor()
        processor.add(SaveNewEntityTask(rental))
        processor.process()
        # Return Result
        return {FieldKey.SUCCESS: rental}

    def read(rentalId):
        # Validate in persistence level
        validatorResponse = RentalValidator.validateRead(rentalId)
        if FieldKey.ERROR in validatorResponse:
            return validatorResponse
        # Read Entity
        rental = ReadOnlyAccess.getEntityCopy(Rental, rentalId)
        # Return Result
        return {FieldKey.SUCCESS: rental}

    def update(updatedRental):
        # Validate in persistence level
        validatorResponse = RentalValidator.validateUpdate(updatedRental)
        if FieldKey.ERROR in validatorResponse:
            return validatorResponse
        # Create and process Tasks
        processor = TaskProcessor()
        processor.add(UpdateEntityTask(Rental, RentalService.mergeRentals, updatedRental))
        processor.process()
        # Return Result
        rental = ReadOnlyAccess.getEntityCopy(Rental, updatedRental.id)
        return {FieldKey.SUCCESS: rental}

    def readAll(customerId):
        # Validate in persistence level
        validatorResponse = RentalValidator.validateReadAll(customerId)
        if FieldKey.ERROR in validatorResponse:
            return validatorResponse
        # Read Entities
        searchFilter = {"customer": customerId}
        rentalList = ReadOnlyAccess.getEntityListCopy(Rental, searchFilter)
        # Return Result
        return {FieldKey.SUCCESS: rentalList}

    def query(query):
        pass

    def mergeRentals(original, new):
        original.start = new.start if new.start is not None else original.start
        original.end = new.end if new.end is not None else original.end
        original.rent = new.rent if new.rent is not None else original.rent
        original.agent = new.agent if new.agent is not None else original.agent
        original.status = new.status if new.status is not None else original.status
        return original
