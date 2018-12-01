import copy

from common.converter.ViewingConverter import ViewingConverter
from common.request_constants.HttpStatus import HttpStatus
from common.request_constants.FieldKey import FieldKey
from common.Error import Error
from common.validator.persistence.ViewingValidator import ViewingValidator

from database.Repository import Repository
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
        validatorResponse = ViewingValidator.validateUpdateViewing(updatedViewing)
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
        #Needs Impl
        return ViewingService.readAll(customerId)

    def mergeProperties(original, new):
        original.mainImageId = new.mainImageId if new.mainImageId is not None else original.mainImageId
        original.city = new.city if new.city is not None else original.city
        original.province = new.province if new.province is not None else original.province
        original.rent = new.rent if new.rent is not None else original.rent
        original.addr1 = new.addr1 if new.addr1 is not None else original.addr1
        original.addr2 = new.addr2 if new.addr2 is not None else original.addr2
        return original
