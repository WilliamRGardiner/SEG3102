from flask import Flask, request
from flask_restful import Resource, Api
from json import loads

from common.authentification.Authenticator import Authenticator
from common.converter.AccountConverter import AccountConverter, AccountField
from common.factory.CredentialFactory import CredentialFactory
from common.request_constants.HttpStatus import HttpStatus
from common.request_constants.FieldKey import FieldKey
from common.request_constants.HeaderKey import HeaderKey
from common.utils.ResponseFormatter import ResponseFormatter
from common.utils.IdGenerator import IdGenerator
from common.validator.resource.AccountValidator import AccountValidator

from domain.Account import Account, AccountType
from service.AccountService import AccountService

'''Routes incoming calls to the AccountController'''
class AgentRouter(Resource):
    def post(self):
        try:
            data = request.data.decode('utf8')
        except:
            data = request.data
        return AccountController.create(loads(data), AccountType.AGENT)

'''Routes incoming calls to the AccountController'''
class AgentIdRouter(Resource):
    def get(self, agentId):
        return AccountController.read(agentId)

    def put(self, agentId):
        try:
            data = request.data.decode('utf8')
        except:
            data = request.data
        return AccountController.update(agentId, loads(data))

    def delete(self, agentId):
        return AccountController.delete(agentId)

'''Routes incoming calls to the AccountController'''
class CustomerRouter(Resource):
    def post(self):
        try:
            data = request.data.decode('utf8')
        except:
            data = request.data
        return AccountController.create(loads(data), AccountType.CUSTOMER)

'''Routes incoming calls to the AccountController'''
class CustomerIdRouter(Resource):
    def get(self, customerId):
        return AccountController.read(customerId)

    def put(self, customerId):
        return AccountController.update(customerId, loads(request.data))

    def delete(self, customerId):
        return AccountController.delete(customerId)

'''Routes incoming calls to the AccountController'''
class OwnerRouter(Resource):
    def post(self):
        return AccountController.create(loads(request.data), AccountType.OWNER)

'''Routes incoming calls to the AccountController'''
class OwnerIdRouter(Resource):
    def get(self, ownerId):
        return AccountController.read(ownerId)

    def put(self, ownerId):
        return AccountController.update(ownerId, loads(request.data))

    def delete(self, ownerId):
        return AccountController.delete(ownerId)

'''
Authenticates Caller,
calidates incoming resources and converts them to Domain Objects,
calls the Service layer to manage the persistence operations,
returns the response from the Service layer.
'''
class AccountController:

    '''Creates an Account'''
    def create(accountResource, accountType):
        # Authenticate
        authenticator = Authenticator(request.headers.get(HeaderKey.TOKEN)).allowAgent()
        authentification = authenticator.authenticate()
        if FieldKey.ERROR in authentification:
            return ResponseFormatter.getFormattedValidatorResponse(authentification)
        # Validate Resource
        accountResourceValidation = AccountValidator.validateCreate(accountResource)
        if FieldKey.ERROR in accountResourceValidation:
            return ResponseFormatter.getFormattedValidatorResponse(accountResourceValidation)
        # Create Domain Instance
        account = AccountConverter.toDomain(accountResource)
        account.id = IdGenerator.generate()
        account.type = accountType
        credential = CredentialFactory.createDomain(account.id, accountResource[AccountField.PASSWORD])
        # Call Service Layer
        response = AccountService.create(account, credential)
        return ResponseFormatter.getFormmattedServiceResponse(AccountConverter.toResource, response)

    '''Reads an Account'''
    def read(accountId):
        # Authenticate
        authenticator = Authenticator(request.headers.get(HeaderKey.TOKEN)).allowAgent().allowCustomer(accountId).allowOwner(accountId)
        authentification = authenticator.authenticate()
        if FieldKey.ERROR in authentification:
            return ResponseFormatter.getFormattedValidatorResponse(authentification)
        # Call Service Layer
        response = AccountService.read(accountId)
        return ResponseFormatter.getFormmattedServiceResponse(AccountConverter.toResource, response)

    '''Updates an Account'''
    def update(accountId, accountResource):
        # Authenticate
        authenticator = Authenticator(request.headers.get(HeaderKey.TOKEN)).allowAgent().allowCustomer(accountId).allowOwner(accountId)
        authentification = authenticator.authenticate()
        if FieldKey.ERROR in authentification:
            return ResponseFormatter.getFormattedValidatorResponse(authentification)
        # Validate Resource
        accountResourceValidation = AccountValidator.validateUpdate(accountResource)
        if FieldKey.ERROR in accountResourceValidation:
            return ResponseFormatter.getFormattedValidatorResponse(accountResourceValidation)
        # Create Domain Instance
        account = AccountConverter.toDomain(accountResource)
        account.id = accountId
        credential = CredentialFactory.createDomain(account.id, accountResource[AccountField.PASSWORD])
        # Call Service Layer
        response = AccountService.update(account, credential)
        return ResponseFormatter.getFormmattedServiceResponse(AccountConverter.toResource, response)

    '''Deletes an Account'''
    def delete(accountId):
        # Authenticate
        authenticator = Authenticator(request.headers.get(HeaderKey.TOKEN)).allowAgent().allowCustomer(accountId).allowOwner(accountId)
        authentification = authenticator.authenticate()
        if FieldKey.ERROR in authentification:
            return ResponseFormatter.getFormattedValidatorResponse(authentification)
        # Call Service Layer
        response = AccountService.delete(accountId)
        return ResponseFormatter.getFormmattedServiceResponse(AccountConverter.toResource, response)
