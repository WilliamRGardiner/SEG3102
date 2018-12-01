from .Repository import Repository
import copy

class ReadOnlyAccess():
    def getEntityCopy(cEntity, entityId):
        session = Repository.Session()
        entity = session.query(cEntity).filter_by(id=entityId).one_or_none()
        entityCopy = copy.deepcopy(entity)
        session.rollback()
        return entityCopy

    def getEntityListCopy(cEntity, filter={}):
        session = Repository.Session()
        entityList = session.query(cEntity).filter_by(**filter).all()
        copyList = []
        for entity in entityList:
            copyList.append(copy.deepcopy(entity))
        return copyList
