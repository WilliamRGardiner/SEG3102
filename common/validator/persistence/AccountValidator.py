from .PersistenceValidator import PersistenceValidator
from domain.Account import Account
from domain.Property import Property
from domain.Rental import Rental, RentalStatus
from common.utils.Date import Date
from common.validator.BaseValidator import BaseValidator
from database.ReadOnlyAccess import ReadOnlyAccess

class AccountValidator():
    def validateCreate(account):
        errors = []
        return BaseValidator.getValidationMessage(AccountValidator.checkUniqueness(errors, account))

    def validateRead(accountId):
        errors = []
        if not PersistenceValidator.checkExists(Account, accountId):
            errors.append(PersistenceValidator.entityDoesNotExist("Account", "id", accountId))
        return BaseValidator.getValidationMessage(errors)

    def validateUpdateAccount(account):
        errors = []
        if PersistenceValidator.checkExists(Account, account.id):
            original = ReadOnlyAccess.getEntityCopy(Account, account.id)
        else:
            original = Account()
            errors.append(PersistenceValidator.entityDoesNotExist("Account", "id", account.id))
        return BaseValidator.getValidationMessage(AccountValidator.checkUniqueness(errors, account, original))

    def validateDelete(accountId):
        properties = ReadOnlyAccess.getEntityListCopy(Property, {"ownerId": accountId})

        rentals= ReadOnlyAccess.getEntityListCopy(Rental, {"owner": accountId})
        rentals.extend(ReadOnlyAccess.getEntityListCopy(Rental, {"customer": accountId}))
        rentals.extend(ReadOnlyAccess.getEntityListCopy(Rental, {"agent": accountId}))
        rentals = list(filter(lambda x: Date.after(Date.toDate(x.end), Date.now()) and x.status == RentalStatus.CONFIRMED, rentals))

        viewings = ReadOnlyAccess.getEntityListCopy(Property, {"customerId": accountId})
        viewings = list(filter(lambda x: Date.after(Date.toDate(x.date), Date.now()), rentals))

        if len(properties) > 0:
            errors.append(PersistenceValidator.subEntitiesExist("Account", "Properties", len(properties)))
        if len(rentals) > 0:
            errors.append(PersistenceValidator.activeSubEntitiesExist("Account", "Rentals", len(rentals)))
        if len(viewings) > 0:
            errors.append(PersistenceValidator.activeSubEntitiesExist("Account", "Viewings", len(viewings)))

        return BaseValidator.getValidationMessage(errors)

    def checkUniqueness(errors, account, original=Account()):
        PersistenceValidator.checkField(errors, Account, account, "username", account.username, original.username)
        PersistenceValidator.checkField(errors, Account, account, "email", account.email, original.email)
        return errors
