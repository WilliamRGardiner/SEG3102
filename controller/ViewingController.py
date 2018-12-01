from flask import Flask, request
from flask_restful import Resource, Api
from json import loads

from common.converter.ViewingConverter import ViewingConverter, ViewingField
from common.request_constants.HttpStatus import HttpStatus
from common.request_constants.FieldKey import FieldKey
from common.utils.ResponseFormatter import ResponseFormatter
from common.utils.IdGenerator import IdGenerator
from common.validator.resource.ViewingValidator import ViewingValidator

from domain.Viewing import Viewing
from service.ViewingService import ViewingService

'''Routes incoming calls to the ViewingController'''
class ViewingRouter(Resource):
    def get(self, customerId):
        return ViewingController.getAll(customerId)

'''Routes incoming calls to the ViewingController'''
class ViewingIdRouter(Resource):
    def post(self, customerId, viewingId):
        # Viewing ID is actually a Property ID for this call
        return ViewingController.create(customerId, viewingId, loads(request.data))

    def get(self, customerId, viewingId):
        return ViewingController.read(customerId, viewingId)

    def put(self, customerId, viewingId):
        return ViewingController.update(customerId, viewingId, loads(request.data))

    def delete(self, customerId, viewingId):
        return ViewingController.delete(customerId, viewingId)

'''Routes incoming calls to the ViewingController'''
class ViewingListRouter(Resource):
    def get(self, customerId):
        return ViewingController.getLsid(customerId)

'''
Authenticates Caller,
calidates incoming resources and converts them to Domain Objects,
calls the Service layer to manage the persistence operations,
returns the response from the Service layer.
'''
class ViewingController:

    '''Creates an Viewing'''
    def create(customerId, propertyId, viewingResource):
        # Authenticate
        authenticator = Authenticator(request.headers.get(HeaderKey.TOKEN)).allowAgent().allowCustomer(customerId)
        authentification = authenticator.authenticate()
        if FieldKey.ERROR in authentification:
            return ResponseFormatter.getFormattedValidatorResponse(authentification)
        # Validate Resource
        viewingResourceValidation = ViewingValidator.validateCreate(viewingResource)
        if FieldKey.ERROR in viewingResourceValidation:
            return ResponseFormatter.getFormattedValidatorResponse(viewingResourceValidation)
        # Create Domain Instance
        viewing = ViewingConverter.toDomain(viewingResource)
        viewing.id = IdGenerator.generate()
        viewing.customerId = customerId
        viewing.propertyId = propertyId
        # Call Service Layer
        response = ViewingService.create(viewing)
        return ResponseFormatter.getFormmattedServiceResponse(ViewingConverter.toResource, response)

    '''Reads an Viewing'''
    def read(customerId, viewingId):
        # Authenticate
        authenticator = Authenticator(request.headers.get(HeaderKey.TOKEN)).allowAgent().allowCustomer(customerId)
        authentification = authenticator.authenticate()
        if FieldKey.ERROR in authentification:
            return ResponseFormatter.getFormattedValidatorResponse(authentification)
        # Call Service Layer
        response = ViewingService.read(customerId, viewingId)
        return ResponseFormatter.getFormmattedServiceResponse(ViewingConverter.toResource, response)

    '''Gets all Viewings for a Customer'''
    def getAll(customerId):
        # Authenticate
        authenticator = Authenticator(request.headers.get(HeaderKey.TOKEN)).allowAgent().allowCustomer(customerId)
        authentification = authenticator.authenticate()
        if FieldKey.ERROR in authentification:
            return ResponseFormatter.getFormattedValidatorResponse(authentification)
        # Call Service Layer
        response = ViewingService.readAll(customerId)
        return ResponseFormatter.getFormmattedServiceListResponse(ViewingConverter.toResource, response)

    '''Gets all upcoming viewings for a Customer'''
    def getList(customerId):
        # Authenticate
        authenticator = Authenticator(request.headers.get(HeaderKey.TOKEN)).allowAgent().allowCustomer(customerId)
        authentification = authenticator.authenticate()
        if FieldKey.ERROR in authentification:
            return ResponseFormatter.getFormattedValidatorResponse(authentification)
        # Call Service Layer
        response = ViewingService.getList(customerId)
        return ResponseFormatter.getFormmattedServiceListResponse(ViewingConverter.toResource, response)

    '''Updates an Viewing'''
    def update(customerId, viewingId, viewingResource):
        # Authenticate
        authenticator = Authenticator(request.headers.get(HeaderKey.TOKEN)).allowAgent().allowCustomer(customerId)
        authentification = authenticator.authenticate()
        if FieldKey.ERROR in authentification:
            return ResponseFormatter.getFormattedValidatorResponse(authentification)
        # Validate Resource
        viewingResourceValidation = ViewingValidator.validateUpdate(viewingResource)
        if FieldKey.ERROR in viewingResourceValidation:
            return ResponseFormatter.getFormattedValidatorResponse(viewingResourceValidation)
        # Create Domain Instance
        viewing = ViewingConverter.toDomain(viewingResource)
        viewing.id = viewingId
        # Call Service Layer
        response = ViewingService.update(viewing)
        return ResponseFormatter.getFormmattedServiceResponse(ViewingConverter.toResource, response)

    '''Deletes an Viewing'''
    def delete(customerId, viewingId):
        # Authenticate
        authenticator = Authenticator(request.headers.get(HeaderKey.TOKEN)).allowAgent().allowCustomer(customerId)
        authentification = authenticator.authenticate()
        if FieldKey.ERROR in authentification:
            return ResponseFormatter.getFormattedValidatorResponse(authentification)
        # Call Service Layer
        response = ViewingService.delete(customerId, viewingId)
        return ResponseFormatter.getFormmattedServiceResponse(ViewingConverter.toResource, response)
