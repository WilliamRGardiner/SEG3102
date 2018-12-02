from .PersistenceValidator import PersistenceValidator
from domain.Account import Account, AccountType
from domain.Property import Property
from domain.Viewing import Viewing
from domain.Rental import Rental, RentalStatus
from common.utils.Date import Date
from common.validator.BaseValidator import BaseValidator
from database.ReadOnlyAccess import ReadOnlyAccess

class PropertyValidator():
    def validateCreate(property):
        errors = []
        if not PersistenceValidator.checkExists(Account, property.ownerId):
            errors.append(PersistenceValidator.entityDoesNotExist("Owner", "id", property.ownerId))
        elif not ReadOnlyAccess.getEntityCopy(Account, property.ownerId).type == AccountType.OWNER:
            errors.append(PersistenceValidator.entityDoesNotExist("Owner", "id", property.ownerId))
        return BaseValidator.getValidationMessage(PropertyValidator.checkUniqueness(errors, property))

    def validateRead(propertyId):
        errors = []
        if not PersistenceValidator.checkExists(Property, propertyId):
            errors.append(PersistenceValidator.entityDoesNotExist("Property", "id", propertyId))
        return BaseValidator.getValidationMessage(errors)

    def validateUpdate(ownerId, property):
        errors = []
        if PersistenceValidator.checkExists(Property, property.id):
            original = ReadOnlyAccess.getEntityCopy(Property, property.id)
            PropertyValidator.checkOwner(errors, ownerId, property.id)
        else:
            original = Property()
            errors.append(PersistenceValidator.entityDoesNotExist("Property", "id", property.id))
        return BaseValidator.getValidationMessage(PropertyValidator.checkUniqueness(errors, property, original))

    def validateDelete(ownerId, propertyId):
        errors = []
        if not PersistenceValidator.checkExists(Property, propertyId):
            errors.append(PersistenceValidator.entityDoesNotExist("Property", "id", propertyId))
        else:
            PropertyValidator.checkOwner(errors, ownerId, propertyId)
            rentals = ReadOnlyAccess.getEntityListCopy(Rental, {"property": propertyId})
            viewings = ReadOnlyAccess.getEntityListCopy(Viewing, {"propertyId": propertyId})
            rentals = list(filter(lambda x: Date.after(Date.toDate(x.end), Date.now()) and x.status == RentalStatus.CONFIRMED, rentals))
            viewings = list(filter(lambda x: Date.after(Date.toDate(x.date), Date.now()), viewings))
            if len(rentals) > 0:
                errors.append(PersistenceValidator.activeSubEntitiesExist("Property", "Rentals", len(rentals)))
            if len(viewings) > 0:
                errors.append(PersistenceValidator.activeSubEntitiesExist("Property", "Viewings", len(viewings)))
        return BaseValidator.getValidationMessage(errors)

    def validateReadAll(ownerId):
        errors = []
        if not PersistenceValidator.checkExists(Account, ownerId):
            errors.append(PersistenceValidator.entityDoesNotExist("Owner", "id", ownerId))
        elif not ReadOnlyAccess.getEntityCopy(Account, ownerId).type == AccountType.OWNER:
            errors.append(PersistenceValidator.entityDoesNotExist("Owner", "id", ownerId))
        return BaseValidator.getValidationMessage(errors)

    def validateHistory(ownerId, start, end):
        return PropertyValidator.validateReadAll(ownerId)

    def validateSearch(criteria):
        return []

    def checkUniqueness(errors, property, original=Property()):
        return errors

    def checkOwner(errors, ownerId, propertyId):
        if not ReadOnlyAccess.getEntityCopy(Property, propertyId).ownerId == ownerId:
            errors.append(PersistenceValidator.linkedDomainNotFoundError("Owner", "Property", ownerId, propertyId))
