from database.Repository import Repository
import copy

'''Updates Entities in the Repository'''
class DetachForeignKeyTask():

    def __init__(self, cEntity, foreignKey, foriegnId):
        self.cEntity = cEntity
        self.foreignKey = foreignKey
        self.foriegnId = foriegnId
        self.entityIdList = []

    def do(self):
        session = Repository.Session()
        searchFilter = {self.foreignKey: self.foriegnId}
        entities = session.query(self.cEntity).filter_by(**searchFilter).all()
        for entity in entities:
            setattr(entity, self.foreignKey, None)
            self.entityIdList += entity.id
        session.commit()

    def undo(self):
        session = Repository.Session()
        for entityId in self.entityIdList:
            session.query(self.cEntity).filter_by(id=entityId).one()
            setattr(entity, self.foreignKey, self.foreignId)
        session.commit()

    def getErrorMessage(self):
        return "Failed to detach entities from entity: " + self.foriegnId
