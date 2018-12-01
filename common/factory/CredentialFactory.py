from common.authentification.PasswordUtility import PasswordUtility
from domain.Credential import Credential

'''Creates a Credential Domain Object'''
class CredentialFactory():

    '''Creates a Credential Domain Object'''
    def createDomain(accountId, password):
        credential = Credential()
        credential.id = accountId
        credential.password = PasswordUtility.getHashedPassword(password)
        return credential
