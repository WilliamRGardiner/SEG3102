from domain.Session import Session

'''Converts Sessions'''
class SessionConverter():
    '''Creates the Resource returned to the Caller'''
    def toResource(session):
        sessionResource = {
            SessionField.TOKEN: session.id
        }
        return sessionResource

'''The known JSON fields'''
class SessionField():
    TOKEN = "session_token"
