from .PersistenceValidator import PersistenceValidator
from domain.Rental import Rental, RentalStatus
from domain.Account import Account
from common.validator.BaseValidator import BaseValidator
from database.ReadOnlyAccess import ReadOnlyAccess

class RentalValidator():
    def validateCreate(rental):
        errors = []
        if not PersistenceValidator.checkExists(Account, rental.customer):
            errors.append(PersistenceValidator.entityDoesNotExist("Customer", "id", rental.customer))
        elif not ReadOnlyAccess.getEntityCopy(Account, rental.customer).type == AccountType.CUSTOMER:
            errors.append(PersistenceValidator.entityDoesNotExist("Customer", "id", rental.customer))
        if not PersistenceValidator.checkExists(Account, rental.owner):
            errors.append(PersistenceValidator.entityDoesNotExist("Owner", "id", rental.owner))
        elif not ReadOnlyAccess.getEntityCopy(Account, rental.owner).type == AccountType.OWNER:
            errors.append(PersistenceValidator.entityDoesNotExist("Owner", "id", rental.owner))
        if not PersistenceValidator.checkExists(Property, rental.property):
            errors.append(PersistenceValidator.entityDoesNotExist("Property", "id", rental.property))
        return BaseValidator.getValidationMessage(RentalValidator.checkUniqueness(errors, rental))

    def validateRead(rentalId):
        errors = []
        if not PersistenceValidator.checkExists(Rental, rentalId):
            errors.append(PersistenceValidator.entityDoesNotExist("Rental", "id", rentalId))
        return errors

    def validateUpdate(rental):
        errors = []
        if PersistenceValidator.checkExists(Rental, rentalId):
            original = ReadOnlyAccess.getEntityCopy(Rental, rental.id)
        else:
            original = Rental()
            errors.append(PersistenceValidator.entityDoesNotExist("Rental", "id", rental.id))
        return BaseValidator.getValidationMessage(RentalValidator.checkUniqueness(errors, rental, original))

    def validateDelete(rentalId):
        errors = RentalValidator.validateRead(rentalId)
        rental = ReadOnlyAccess.getEntityCopy(Rental, rentalId)
        if Date.after(Date.toDate(rental.end), Date.now()) and rental.status == RentlStatus.CONFIRMED:
            errors.append(PersistenceValidator.entityActive("Rental", rentalId))
        return BaseValidator.getValidationMessage(errors)

    def validateReadAll(customerId):
        errors = []
        if not PersistenceValidator.checkExists(Account, customerId):
            errors.append(PersistenceValidator.entityDoesNotExist("Customer", "id", customerId))
        return BaseValidator.getValidationMessage(errors)

    def validateQuery(query):
        return BaseValidator.getValidationMessage([])

    def checkUniqueness(errors, rental, original=Rental()):
        return errors
