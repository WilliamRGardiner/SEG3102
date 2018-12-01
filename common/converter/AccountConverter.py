from domain.Account import Account

'''Converts Accounts'''
class AccountConverter():

    '''Creates the Domain Object used internally'''
    def toDomain(accountResource):
        account = Account()
        account.id = accountResource[AccountField.ID] if AccountField.ID in accountResource else None
        account.username = accountResource[AccountField.USERNAME] if AccountField.USERNAME in accountResource else None
        account.email = accountResource[AccountField.EMAIL] if AccountField.EMAIL in accountResource else None
        account.type = accountResource[AccountField.TYPE] if AccountField.TYPE in accountResource else None
        account.firstName = accountResource[AccountField.FIRST_NAME] if AccountField.FIRST_NAME in accountResource else None
        account.lastName = accountResource[AccountField.LAST_NAME] if AccountField.LAST_NAME in accountResource else None
        account.dateOfBirth = accountResource[AccountField.DATE_OF_BIRTH] if AccountField.DATE_OF_BIRTH in accountResource else None
        return account

    '''Creates the Resource returned to the Caller'''
    def toResource(account):
        accountResource = {
            AccountField.ID: account.id,
            AccountField.USERNAME: account.username,
            AccountField.EMAIL: account.email,
            AccountField.FIRST_NAME: account.firstName,
            AccountField.LAST_NAME: account.lastName,
            AccountField.DATE_OF_BIRTH: account.dateOfBirth
        }
        return accountResource

'''The known JSON fields'''
class AccountField():
    ID = "id"
    USERNAME = "username"
    EMAIL = "email"
    TYPE = "type"
    FIRST_NAME = "first_name"
    LAST_NAME = "last_name"
    DATE_OF_BIRTH = "date_of_birth"
    PASSWORD = "password"
