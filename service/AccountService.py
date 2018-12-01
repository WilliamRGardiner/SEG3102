import copy

from database.Repository import Repository
from database.ReadOnlyAccess import ReadOnlyAccess

from common.request_constants.HttpStatus import HttpStatus
from common.request_constants.FieldKey import FieldKey
from common.Error import Error
from common.validator.persistence.AccountValidator import AccountValidator

from domain.Account import Account

from database.ReadOnlyAccess import ReadOnlyAccess
from task.TaskProcessor import TaskProcessor
from task.repository.SaveNewEntityTask import SaveNewEntityTask
from task.repository.UpdateEntityTask import UpdateEntityTask
from task.repository.DeleteEntityTask import DeleteEntityTask
from task.repository.DetachForeignKeyTask import DetachForeignKeyTask

'''
Validates Accounts agains the persistence layer,
reads Accounts from the persistence layer,
and performs operations on Accounts via Tasks
'''
class AccountService():
    def create(account, credential):
        # Validate in persistence level
        validatorResponse = AccountValidator.validateCreate(account)
        if FieldKey.ERROR in validatorResponse:
            return validatorResponse
        # Create and process Tasks
        processor = TaskProcessor()
        processor.add(SaveNewEntityTask(account))
        processor.add(SaveNewEntityTask(credential))
        processor.process()
        # Return Result
        return {FieldKey.SUCCESS: account}

    def read(accountId):
        # Validate in persistence level
        validatorResponse = AccountValidator.validateRead(accountId)
        if FieldKey.ERROR in validatorResponse:
            return validatorResponse
        # Create and process Tasks
        account = ReadOnlyAccess.getEntityCopy(Account, accountId)
        # Return Result
        return {FieldKey.SUCCESS: account}

    def update(updatedAccount, updatedCredential):
        # Validate in persistence level
        validatorResponse = AccountValidator.validateUpdate(updatedAccount)
        if FieldKey.ERROR in validatorResponse:
            return validatorResponse
        # Create and process Tasks
        processor = TaskProcessor()
        processor.add(UpdateEntityTask(Account, AccountService.mergeAccounts, updatedAccount))
        processor.add(UpdateEntityTask(Credential, AccountService.mergeCredentials, updatedCredential))
        processor.process()
        # Return Result
        account = ReadOnlyAccess.getEntityCopy(Account, updatedAccount.id)
        return {FieldKey.SUCCESS: account}

    def delete(accountId):
        # Validate in persistence level
        validatorResponse = AccountValidator.validateDelete(accountId)
        if FieldKey.ERROR in validatorResponse:
            return validatorResponse
        # Get return copy, before delete
        account = ReadOnlyAccess.getEntityCopy(Account, accountId)
        # Create and process Tasks
        processor = TaskProcessor()
        processor.add(DetachForeignKeyTask(Rental, "customer", accountId))
        processor.add(DetachForeignKeyTask(Rental, "agent", accountId))
        processor.add(DetachForeignKeyTask(Viewing, "customerId", accountId))
        processor.add(DeleteEntityTask(Credential, accountId))
        processor.add(DeleteEntityTask(Account, accountId))
        processor.process()
        # Return Result
        return {FieldKey.SUCCESS: account}

    def mergeAccounts(original, new):
        original.firstName = new.firstName if new.firstName is not None else original.firstName
        original.lastName = new.lastName if new.lastName is not None else original.lastName
        original.dateOfBirth = new.dateOfBirth if new.dateOfBirth is not None else original.dateOfBirth
        return original

    def mergeCredentials(original, new):
        original.password = new.password if new.password is not None else original.password
        return original
