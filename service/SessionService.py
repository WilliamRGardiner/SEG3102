import copy

from database.Repository import Repository
from database.ReadOnlyAccess import ReadOnlyAccess

from common.request_constants.HttpStatus import HttpStatus
from common.request_constants.FieldKey import FieldKey
from common.Error import Error
from common.validator.persistence.SessionValidator import SessionValidator

from domain.Session import Session

from database.ReadOnlyAccess import ReadOnlyAccess
from task.TaskProcessor import TaskProcessor
from task.repository.SaveNewEntityTask import SaveNewEntityTask
from task.repository.UpdateEntityTask import UpdateEntityTask
from task.repository.DeleteEntityTask import DeleteEntityTask
from task.repository.DetachForeignKeyTask import DetachForeignKeyTask

'''
Handles login and logout on the persistence layer
'''
class SessionService():
    def login(session, password):
        # Validate in persistence level
        validatorResponse = SessionValidator.validateCreate(session.username, password)
        if FieldKey.ERROR in validatorResponse:
            return validatorResponse

        # Create and process Tasks
        processor = TaskProcessor()
        sessions = ReadOnlyAccess.getEntityListCopy(Session, {"username": session.username})
        if(len(sessions) > 1):
            raise Exception("Multiple sessions for user")
        elif(len(sessions) == 1):
            if SessionUtility.isExpired(sessions[0]):
                processor.add(DeleteEntityTask(Session, sessions[0].id))
                processor.add(SaveNewEntityTask(session))
            else:
                session.id = sessions[0].id
                processor.add(UpdateEntityTask(Session, SessionService.mergeSessions, session))
        else:
            processor.add(SaveNewEntityTask(session))
        processor.process()
        returnSession = ReadOnlyAccess.getEntityCopy(Session, session.id)
        # Return Result
        return {FieldKey.SUCCESS: returnSession}

    def logout(sessionToken):
        # Validate in persistence level
        validatorResponse = SessionValidator.validateRead(sessionToken)
        if FieldKey.ERROR in validatorResponse:
            return validatorResponse
        session = ReadOnlyAccess.getEntityCopy(Session, sessionToken)
        # Create and process Tasks
        processor = TaskProcessor()
        processor.add(DeleteEntityTask(Session, sessionToken))
        processor.process()
        # Return Result
        return {FieldKey.SUCCESS: session}

    def mergeSessions(original, new):
        original.lastUsed = new.lastUsed
        return original
