import copy

from common.converter.ViewingConverter import ViewingConverter
from common.request_constants.HttpStatus import HttpStatus
from common.request_constants.FieldKey import FieldKey
from common.Error import Error
from common.utils.Date import Date
from common.validator.persistence.ViewingValidator import ViewingValidator

from database.ReadOnlyAccess import ReadOnlyAccess
from domain.Viewing import Viewing

from task.TaskProcessor import TaskProcessor
from task.repository.SaveNewEntityTask import SaveNewEntityTask
from task.repository.UpdateEntityTask import UpdateEntityTask
from task.repository.DeleteEntityTask import DeleteEntityTask

'''
Validates Viewings agains the persistence layer,
reads Viewings from the persistence layer,
and performs operations on Viewings via Tasks
'''
class ViewingService():
    def create(viewing):
        # Validate in persistence level
        validatorResponse = ViewingValidator.validateCreate(viewing)
        if FieldKey.ERROR in validatorResponse:
            return validatorResponse
        # Create and process Tasks
        processor = TaskProcessor()
        processor.add(SaveNewEntityTask(viewing))
        processor.process()
        # Return Result
        return {FieldKey.SUCCESS: viewing}

    def read(customerId, viewingId):
        # Validate in persistence level
        validatorResponse = ViewingValidator.validateRead(customerId, viewingId)
        if FieldKey.ERROR in validatorResponse:
            return validatorResponse
        # Create and process Tasks
        viewing = ReadOnlyAccess.getEntityCopy(Viewing, viewingId)
        # Return Result
        return {FieldKey.SUCCESS: viewing}

    def update(updatedViewing):
        # Validate in persistence level
        validatorResponse = ViewingValidator.validateUpdate(updatedViewing)
        if FieldKey.ERROR in validatorResponse:
            return validatorResponse
        # Create and process Tasks
        processor = TaskProcessor()
        processor.add(UpdateEntityTask(Viewing, ViewingService.mergeViewings, updatedViewing))
        processor.process()
        # Return Result
        viewing = ReadOnlyAccess.getEntityCopy(Viewing, updatedViewing.id)
        return {FieldKey.SUCCESS: viewing}

    def delete(customerId, viewingId):
        # Validate in persistence level
        validatorResponse = ViewingValidator.validateDelete(customerId, viewingId)
        if FieldKey.ERROR in validatorResponse:
            return validatorResponse
        # Get return copy, before delete
        viewing = ReadOnlyAccess.getEntityCopy(Viewing, viewingId)
        # Create and process Tasks
        processor = TaskProcessor()
        processor.add(DeleteEntityTask(Viewing, viewingId))
        processor.process()
        # Return Result
        return {FieldKey.SUCCESS: viewing}

    def readAll(customerId):
        # Validate in persistence level
        validatorResponse = ViewingValidator.validateReadAll(customerId)
        if FieldKey.ERROR in validatorResponse:
            return validatorResponse
        # Read Entities
        searchFilter = {"customerId": customerId}
        viewingList = ReadOnlyAccess.getEntityListCopy(Viewing, searchFilter)
        # Return Result
        return {FieldKey.SUCCESS: viewingList}

    def readList(customerId):
        # Validate in persistence level
        validatorResponse = ViewingValidator.validateReadAll(customerId)
        if FieldKey.ERROR in validatorResponse:
            return validatorResponse
        # Read Entities
        searchFilter = {"customerId": customerId}
        viewingList = ReadOnlyAccess.getEntityListCopy(Viewing, searchFilter)
        viewingList = list(filter(lambda x: Date.after(Date.toDate(x.date), Date.now()), viewingList))
        return {FieldKey.SUCCESS: viewingList}

    def mergeViewings(original, new):
        original.date = new.date if new.date is not None else original.date
        original.comment = new.comment if new.comment is not None else original.comment
        return original
