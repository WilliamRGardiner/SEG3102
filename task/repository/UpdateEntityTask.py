from database.Repository import Repository
import copy

'''Updates Entities in the Repository'''
class UpdateEntityTask():

    def __init__(self, cEntity, fMerge, modifiedEntity):
        self.cEntity = cEntity
        self.modifiedEntity = modifiedEntity
        self.fMerge = fMerge

    def do(self):
        session = Repository.Session()
        entity = session.query(self.cEntity).filter_by(id=self.modifiedEntity.id).one()
        self.original = copy.deepcopy(entity)
        self.fMerge(entity, self.modifiedEntity)
        session.commit()

    def undo(self):
        session = Repository.Session()
        entity = session.query(self.cEntity).filter_by(id=self.modifiedEntity.id).one()
        self.fMerge(entity, self.original)
        session.commit()

    def getErrorMessage(self):
        return "Failed to save entity: \n" + self.modifiedEntity
