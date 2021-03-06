from flask import Flask, request
from flask_restful import Resource, Api
from json import loads

from common.authentification.Authenticator import Authenticator
from common.converter.RentalConverter import RentalConverter, RentalField
from common.request_constants.HttpStatus import HttpStatus
from common.request_constants.FieldKey import FieldKey
from common.request_constants.HeaderKey import HeaderKey
from common.utils.ResponseFormatter import ResponseFormatter
from common.utils.IdGenerator import IdGenerator
from common.validator.resource.RentalValidator import RentalValidator

from domain.Rental import Rental, RentalStatus
from service.RentalService import RentalService

'''Routes incoming calls to the RentalController'''
class RentalRouter(Resource):
    def post(self):
        try:
            data = request.data.decode('utf8')
        except:
            data = request.data
        return RentalController.create(loads(data))

'''Routes incoming calls to the RentalController'''
class RentalIdRouter(Resource):
    def get(self, rentalId):
        return RentalController.read(rentalId)

    def put(self, rentalId):
        try:
            data = request.data.decode('utf8')
        except:
            data = request.data
        return RentalController.update(rentalId, loads(data))

'''Routes incoming calls to the RentalController'''
class RentalConfirmRouter(Resource):
    def put(self, rentalId):
        return RentalController.confirm(rentalId)

'''Routes incoming calls to the RentalController'''
class RentalDenyRouter(Resource):
    def put(self, rentalId):
        return RentalController.deny(rentalId)

'''Routes incoming calls to the RentalController'''
class RentalCancelRouter(Resource):
    def put(self, rentalId):
        return RentalController.cancel(rentalId)

'''Routes incoming calls to the RentalController'''
class RentalQueryRouter(Resource):
    def put(self):
        try:
            data = request.data.decode('utf8')
        except:
            data = request.data
        return RentalController.query(loads(data))

'''Routes incoming calls to the RentalController'''
class RentalCustomerRouter(Resource):
    def get(self, customerId):
        return RentalController.readAll(customerId)

'''
Authenticates Caller,
calidates incoming resources and converts them to Domain Objects,
calls the Service layer to manage the persistence operations,
returns the response from the Service layer.
'''
class RentalController():
    def create(rentalResource):
        # Authenticate
        authenticator = Authenticator(request.headers.get(HeaderKey.TOKEN)).allowAgent().allowCustomer(rentalResource[RentalField.CUSTOMER])
        authentification = authenticator.authenticate()
        if FieldKey.ERROR in authentification:
            return ResponseFormatter.getFormattedValidatorResponse(authentification)
        # Validate Resource
        rentalResourceValidation = RentalValidator.validateCreate(rentalResource)
        if FieldKey.ERROR in rentalResourceValidation:
            return ResponseFormatter.getFormattedValidatorResponse(rentalResourceValidation)
        # Create Domain Instance
        rental = RentalConverter.toDomain(rentalResource)
        rental.id = IdGenerator.generate()
        rental.status = RentalStatus.PROPOSED
        # Call Service Layer
        response = RentalService.create(rental)
        return ResponseFormatter.getFormmattedServiceResponse(RentalConverter.toResource, response)

    def update(rentalId, rentalResource):
        # Authenticate
        authenticator = Authenticator(request.headers.get(HeaderKey.TOKEN)).allowAgent().allowOwnerOf(Rental, "customer", rentalId)
        authentification = authenticator.authenticate()
        if FieldKey.ERROR in authentification:
            return ResponseFormatter.getFormattedValidatorResponse(authentification)
        # Validate Resource
        rentalResourceValidation = RentalValidator.validateUpdate(rentalResource)
        if FieldKey.ERROR in rentalResourceValidation:
            return ResponseFormatter.getFormattedValidatorResponse(rentalResourceValidation)
        # Create Domain Instance
        rental = RentalConverter.toDomain(rentalResource)
        rental.id = rentalId
        rental.status = RentalStatus.PROPOSED
        # Call Service Layer
        response = RentalService.update(rental)
        return ResponseFormatter.getFormmattedServiceResponse(RentalConverter.toReso0urce, response)

    def read(rentalId):
        # Authenticate
        authenticator = Authenticator(request.headers.get(HeaderKey.TOKEN)).allowAgent().allowOwnerOf(Rental, "customer", rentalId)
        authentification = authenticator.authenticate()
        if FieldKey.ERROR in authentification:
            return ResponseFormatter.getFormattedValidatorResponse(authentification)
        # Call Service Layer
        response = RentalService.read(rentalId)
        return ResponseFormatter.getFormmattedServiceResponse(RentalConverter.toResource, response)

    def confirm(rentalId):
        # Authenticate
        authenticator = Authenticator(request.headers.get(HeaderKey.TOKEN)).allowAgent()
        authentification = authenticator.authenticate()
        if FieldKey.ERROR in authentification:
            return ResponseFormatter.getFormattedValidatorResponse(authentification)
        # Create Domain Instance
        rental = Rental()
        rental.id = rentalId
        rental.status = RentalStatus.CONFIRMED
        # Call Service Layer
        response = RentalService.update(rental)
        return ResponseFormatter.getFormmattedServiceResponse(RentalConverter.toResource, response)

    def deny(rentalId):
        # Authenticate
        authenticator = Authenticator(request.headers.get(HeaderKey.TOKEN)).allowAgent().allowOwnerOf(Rental, "customer", rentalId)
        authentification = authenticator.authenticate()
        if FieldKey.ERROR in authentification:
            return ResponseFormatter.getFormattedValidatorResponse(authentification)
        # Create Domain Instance
        rental = Rental()
        rental.id = rentalId
        rental.status = RentalStatus.DENIED
        # Call Service Layer
        response = RentalService.update(rental)
        return ResponseFormatter.getFormmattedServiceResponse(RentalConverter.toResource, response)

    def cancel(rentalId):
        # Authenticate
        authenticator = Authenticator(request.headers.get(HeaderKey.TOKEN)).allowAgent()
        authentification = authenticator.authenticate()
        if FieldKey.ERROR in authentification:
            return ResponseFormatter.getFormattedValidatorResponse(authentification)
        # Create Domain Instance
        rental = Rental()
        rental.id = rentalId
        rental.status = RentalStatus.CANCELLED
        # Call Service Layer
        response = RentalService.update(rental)
        return ResponseFormatter.getFormmattedServiceResponse(RentalConverter.toResource, response)

    def query(queryResource):
        # Authenticate
        # Validate Resource
        # Create Domain Instance
        # Call Service Layer
        pass

    def readAll(customerId):
        # Authenticate
        # Validate Resource
        # Create Domain Instance
        # Call Service Layer
        pass
