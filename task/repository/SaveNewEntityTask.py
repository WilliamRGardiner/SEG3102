from database.Repository import Repository

'''Saves Entities tos the Repository'''
class SaveNewEntityTask():

    def __init__(self, entity):
        self.entity = entity

    def do(self):
        session = Repository.Session()
        session.add(self.entity)
        session.commit()

    def undo(self):
        session = Repository.Session()
        session.delete(self.entity)
        session.commit()

    def getErrorMessage(self):
        return "Failed to save entity: \n" + entity
