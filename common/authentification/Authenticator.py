from common.request_constants.FieldKey import FieldKey
from domain.Account import AccountType
from .SessionUtility import SessionUtility

class Authenticator():
    def __init__(self, sessionToken):
        isValid, account = SessionUtility.getAccount(sessionToken)
        self.sessionToken = sessionToken
        self.account = account
        self.isValid = isValid
        self.passed = False

    def allowAgent(self, id=None):
        self.allowAccount(id, AccountType.AGENT)
        return self

    def allowCustomer(self, id=None):
        self.allowAccount(id, AccountType.CUSTOMER)
        return self

    def allowOwner(self, id=None):
        self.allowAccount(id, AccountType.OWNER)
        return self

    def allowAccount(self, id, accountType):
        if self.isValid:
            if self.account.type == accountType:
                if id is None:
                    self.passed = True
                else:
                    self.passed = self.passed or self.account.id == id

    def authenticate(self):
        if not self.isValid:
            return Authenticator.invalidTokenError(self.sessionToken)
        if not self.passed:
            return Authenticator.insufficientPermissionsError()
        return Authenticator.ok()

    def invalidTokenError(token):
        return {FieldKey.ERROR: "Token: "+token+" is invalid or expired."}

    def insufficientPermissionsError():
        return {FieldKey.ERROR: "User has insufficient permissions for this operation."}

    def ok():
        return {FieldKey.SUCCESS: "OK"}
