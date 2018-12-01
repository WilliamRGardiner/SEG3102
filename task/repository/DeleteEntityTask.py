from database.Repository import Repository
import copy

'''Deletes Entities from the Repository'''
class DeleteEntityTask():

    def __init__(self, cEntity, entityId):
        self.cEntity = cEntity
        self.entityId = entityId

    def do(self):
        session = Repository.Session()
        entity = session.query(self.cEntity).filter_by(id=self.entityId).one()
        self.backup = copy.deepcopy(entity)
        session.delete(entity)
        session.commit()

    def undo(self):
        session = Repository.Session()
        session.add(self.backup)
        session.commit()

    def getErrorMessage(self):
        return "Failed to delete entity: \n" + entity
