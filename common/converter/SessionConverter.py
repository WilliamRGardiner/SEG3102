from domain.Session import Session

'''Converts Sessions'''
class SessionConverter():
    '''Creates the Resource returned to the Caller'''
    def toResource(session):
        sessionResource = {
            SessionField.TOKEN: session.id,
            SessionField.ACCOUNT: session.accountId if hasattr(session, 'accountId') else None,
            SessionField.TYPE: session.accountType if hasattr(session, 'accountType') else None
        }
        return sessionResource

'''The known JSON fields'''
class SessionField():
    TOKEN = "session_token"
    ACCOUNT = "account_id"
    TYPE = "account_type"
