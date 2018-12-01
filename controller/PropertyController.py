from flask import Flask, request
from flask_restful import Resource, Api
from json import loads

from common.authentification.Authenticator import Authenticator
from common.converter.PropertyConverter import PropertyConverter, PropertyField
from common.request_constants.HttpStatus import HttpStatus
from common.request_constants.FieldKey import FieldKey
from common.request_constants.HeaderKey import HeaderKey
from common.utils.ResponseFormatter import ResponseFormatter
from common.utils.IdGenerator import IdGenerator
from common.validator.resource.PropertyValidator import PropertyValidator

from domain.Property import Property, PropertyStatus
from service.PropertyService import PropertyService

'''Routes incoming calls to the PropertyController'''
class PropertyRouter(Resource):
    def post(self, ownerId):
        return PropertyController.create(ownerId, loads(request.data))

    def get(self, ownerId):
        return PropertyController.readAll(ownerId)

'''Routes incoming calls to the PropertyController'''
class PropertyIdRouter(Resource):
    def put(self, ownerId, propertyId):
        return PropertyController.update(ownerId, propertyId, loads(request.data))

    def delete(self, ownerId, propertyId):
        return PropertyController.delete(ownerId, propertyId)

'''Routes incoming calls to the PropertyController'''
class PropertySimpleRouter(Resource):
    def get(self, propertyId):
        return PropertyController.read(propertyId)

'''Routes incoming calls to the PropertyController'''
class PropertyHistoryRouter(Resource):
    def get(self, ownerId):
        return PropertyController.history(ownerId)

'''Routes incoming calls to the PropertyController'''
class PropertySearchRouter(Resource):
    def get(self):
        return PropertyController.search()

'''
Authenticates Caller,
calidates incoming resources and converts them to Domain Objects,
calls the Service layer to manage the persistence operations,
returns the response from the Service layer.
'''
class PropertyController(Resource):
    def create(ownerId, propertyResource):
        # Authenticate
        authenticator = Authenticator(request.headers.get(HeaderKey.TOKEN)).allowAgent().allowOwner(ownerId)
        authentification = authenticator.authenticate()
        if FieldKey.ERROR in authentification:
            return ResponseFormatter.getFormattedValidatorResponse(authentification)
        # Validate Resource
        propertyResourceValidation = PropertyValidator.validateCreate(propertyResource)
        if FieldKey.ERROR in propertyResourceValidation:
            return ResponseFormatter.getFormattedValidatorResponse(propertyResourceValidation)
        # Create Domain Instance
        property = PropertyConverter.toDomain(propertyResource)
        property.id = IdGenerator.generate()
        property.ownerId = ownerId
        property.status = PropertyStatus.AVAILABLE
        # Call Service Layer
        response = PropertyService.create(property)
        return ResponseFormatter.getFormmattedServiceResponse(PropertyConverter.toResource, response)

    def read(propertyId):
        # Authenticate
            # All Access
        # Call Service Layer
        response = PropertyService.read(propertyId)
        return ResponseFormatter.getFormmattedServiceResponse(PropertyConverter.toResource, response)

    def update(ownerId, propertyId, propertyResource):
        # Authenticate
        authenticator = Authenticator(request.headers.get(HeaderKey.TOKEN)).allowAgent().allowOwner(ownerId)
        authentification = authenticator.authenticate()
        if FieldKey.ERROR in authentification:
            return ResponseFormatter.getFormattedValidatorResponse(authentification)
        # Validate Resource
        propertyResourceValidation = PropertyValidator.validateUpdate(propertyResource)
        if FieldKey.ERROR in propertyResourceValidation:
            return ResponseFormatter.getFormattedValidatorResponse(propertyResourceValidation)
        # Create Domain Instance
        property = PropertyConverter.toDomain(propertyResource)
        property.id = propertyId
        # Call Service Layer
        response = PropertyService.update(ownerId, property)
        return ResponseFormatter.getFormmattedServiceResponse(PropertyConverter.toResource, response)

    def delete(ownerId, propertyId):
        # Authenticate
        authenticator = Authenticator(request.headers.get(HeaderKey.TOKEN)).allowAgent().allowOwner(ownerId)
        authentification = authenticator.authenticate()
        if FieldKey.ERROR in authentification:
            return ResponseFormatter.getFormattedValidatorResponse(authentification)
        # Call Service Layer
        response = PropertyService.delete(ownerId, propertyId)
        return ResponseFormatter.getFormmattedServiceResponse(PropertyConverter.toResource, response)

    def readAll(ownerId):
        # Authenticate
        authenticator = Authenticator(request.headers.get(HeaderKey.TOKEN)).allowAgent().allowOwner(ownerId)
        authentification = authenticator.authenticate()
        if FieldKey.ERROR in authentification:
            return ResponseFormatter.getFormattedValidatorResponse(authentification)
        # Call Service Layer
        response = PropertyService.readAll(ownerId)
        return ResponseFormatter.getFormmattedServiceListResponse(PropertyConverter.toResource, response)

    def history(ownerId):
        # Authenticate
        authenticator = Authenticator(request.headers.get(HeaderKey.TOKEN)).allowAgent().allowOwner(ownerId)
        authentification = authenticator.authenticate()
        if FieldKey.ERROR in authentification:
            return ResponseFormatter.getFormattedValidatorResponse(authentification)
        # Create Domain Instance
        start = request.args.get('start', default=None, type=str)
        end = request.args.get('end', default=None, type=str)
        # Call Service Layer
        response = PropertyService.history(ownerId, start, end)
        return ResponseFormatter.getFormmattedServiceListResponse(PropertyConverter.toResource, response)

    def search():
        # Authenticate
            # All Access
        # Create Domain Instance
        criteria = {
            "city": request.args.get("city", default=None, type=str),
            "province": request.args.get("prov", default=None, type=str),
            "min": request.args.get("min", default=None, type=int),
            "max": request.args.get("max", default=None, type=int)
        }
        # Call Service Layer
        response = PropertyService.search(criteria)
        return ResponseFormatter.getFormmattedServiceListResponse(PropertyConverter.toResource, response)
