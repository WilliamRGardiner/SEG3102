from .PersistenceValidator import PersistenceValidator
from domain.Account import Account, AccountType
from domain.Viewing import Viewing
from domain.Property import Property
from common.validator.BaseValidator import BaseValidator
from database.ReadOnlyAccess import ReadOnlyAccess

class ViewingValidator():
    def validateCreate(viewing):
        errors = []
        if not PersistenceValidator.checkExists(Account, viewing.customerId):
            errors.append(PersistenceValidator.entityDoesNotExist("Customer", "id", viewing.customerId))
        elif not ReadOnlyAccess.getEntityCopy(Account, viewing.customerId).type == AccountType.CUSTOMER:
            errors.append(PersistenceValidator.entityDoesNotExist("Customer", "id", viewing.customerId))
        if not PersistenceValidator.checkExists(Property, viewing.propertyId):
            errors.append(PersistenceValidator.entityDoesNotExist("Property", "id", viewing.propertyId))
        return BaseValidator.getValidationMessage(ViewingValidator.checkUniqueness(errors, viewing.propertyId))

    def validateRead(customerId, viewingId):
        errors = []
        if not PersistenceValidator.checkExists(Account, customerId):
            errors.append(PersistenceValidator.entityDoesNotExist("Customer", "id", customerId))
        if not PersistenceValidator.checkExists(Viewing, viewingId):
            errors.append(PersistenceValidator.entityDoesNotExist("Viewing", "id", viewingId))
        if not ReadOnlyAccess.getEntityCopy(Viewing, vewingId).customerId == customerId:
            errors.append(PersistenceValidator.linkedDomainNotFoundError("Customer", "Viewing", customerId, viewingId))
        return errors

    def validateUpdate(viewing):
        errors = []
        if not ViewingValidator.viewingExists(viewing.id):
            original = ReadOnlyAccess.getEntityCopy(Viewing, viewing.id)
        else:
            original = Viewing()
            errors.append(PersistenceValidator.entityDoesNotExist("Viewing", "id", viewing.id))
        return BaseValidator.getValidationMessage(ViewingValidator.checkUniqueness(errors, viewing, original))

    def validateDelete(customerId, viewingId):
        return ViewingValidator.validateRead(customerId, viewingId)

    def validateReadAll(customerId):
        errors = []
        if not PersistenceValidator.checkExists(Account, customerId):
            errors.append(PersistenceValidator.entityDoesNotExist("Customer", "id", customerId))
        return BaseValidator.getValidationMessage(errors)

    def validateReadList(customerId):
        return ViewingValidator.validateReadAll(customerId)

    def checkUniqueness(errors, viewing, original=Viewing()):
        return errors
