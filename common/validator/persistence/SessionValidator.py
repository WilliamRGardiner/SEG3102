from .PersistenceValidator import PersistenceValidator
from domain.Account import Account
from domain.Credential import Credential
from common.validator.BaseValidator import BaseValidator
from common.authentification.PasswordUtility import PasswordUtility
from database.ReadOnlyAccess import ReadOnlyAccess

class SessionValidator():
    def validateCreate(username, password):
        errors = []
        accounts = ReadOnlyAccess.getEntityListCopy(Account, {"username": username})
        if len(accounts) > 1:
            raise Exception("Multiple Accounts with Username: " + username)
        elif len(accounts) < 1:
            errors.append(SessionValidator.incorrectUsernameOrPassword())
        else:
            credential = ReadOnlyAccess.getEntityCopy(Credential, accounts[0].id)
            if credential is None or not PasswordUtility.checkHashedPassword(password, credential.password):
                errors.append(SessionValidator.incorrectUsernameOrPassword())
        return BaseValidator.getValidationMessage(errors)

    def validateDelete(sessionId):
        errors = []
        if not PersistenceValidator.checkExists(Session, sessionId):
            errors.append(PersistenceValidator.entityDoesNotExist("Session", "token", sessionId))
        return BaseValidator.getValidationMessage(errors)

    def incorrectUsernameOrPassword():
        return {"field": PersistenceValidator.NO_FIELD, "msg": "Incorrect username or password"}
