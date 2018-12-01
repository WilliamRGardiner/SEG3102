from domain.Session import Session
from common.authentification.SessionUtility import SessionUtility
from common.utils.Date import Date

'''Creates a Session Domain Object'''
class SessionFactory():

    '''Creates a Session Domain Object'''
    def createDomain(username):
        session = Session()
        session.id = SessionUtility.getToken()
        session.username = username
        session.lastUsed = Date.toString(Date.now())
        return session
