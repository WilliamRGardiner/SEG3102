import base64
import os
import properties
import datetime

from common.utils.Date import Date
from database.ReadOnlyAccess import ReadOnlyAccess
from domain.Account import Account
from domain.Session import Session


class SessionUtility():
    def getAccount(sessionToken):
        try:
            session = ReadOnlyAccess.getEntityCopy(Session, sessionToken)
        except:
            return False, None
        if SessionUtility.isExpired(session):
            return False, None
        return True, ReadOnlyAccess.getEntityListCopy(Account, {"username": session.username})[0]

    def isExpired(session):
        return Date.before(Date.toDate(session.lastUsed) + datetime.timedelta(minutes=properties.token_lifespan), Date.now())

    def getToken(numberOfBytes = properties.token_length):
        return base64.b64encode(os.urandom(numberOfBytes)).decode('utf8')
