from flask import Flask, request
from flask_restful import Resource, Api
from json import loads

from common.authentification.Authenticator import Authenticator
from common.converter.ImageConverter import ImageConverter, ImageField
from common.converter.PropertyConverter import PropertyConverter
from common.factory.ImageFactory import ImageFactory
from common.request_constants.HttpStatus import HttpStatus
from common.request_constants.FieldKey import FieldKey
from common.request_constants.HeaderKey import HeaderKey
from common.utils.ResponseFormatter import ResponseFormatter
from common.utils.IdGenerator import IdGenerator
from common.validator.resource.ImageValidator import ImageValidator

from domain.Image import Image
from domain.Property import Property
from service.ImageService import ImageService

'''Routes incoming calls to the ImageController'''
class ImageRouter(Resource):
    def post(self, propertyId):
        return ImageController.add(propertyId)

    def get(self, propertyId):
        return ImageController.readAll(propertyId)

'''Routes incoming calls to the ImageController'''
class ImageIdRouter(Resource):
    def get(self, propertyId, imageId):
        return ImageController.read(propertyId, imageId)

    def put(self, propertyId, imageId):
        return ImageController.update(propertyId, imageId, loads(request.data))

    def delete(self, propertyId, imageId):
        return ImageController.remove(propertyId, imageId)

'''Routes incoming calls to the ImageController'''
class ImageMainRouter(Resource):
    def put(self, propertyId, imageId):
        return ImageController.setMain(propertyId, imageId)

'''
Authenticates Caller,
calidates incoming resources and converts them to Domain Objects,
calls the Service layer to manage the persistence operations,
returns the response from the Service layer.
'''
class ImageController():

    '''Uploads an Image File'''
    def add(propertyId):
        # Authentication
        authenticator = Authenticator(request.headers.get(HeaderKey.TOKEN)).allowAgent().allowOwnerOf(Property, "ownerId", propertyId)
        authentification = authenticator.authenticate()
        if FieldKey.ERROR in authentification:
            return ResponseFormatter.getFormattedValidatorResponse(authentification)
        # Create Domain Instance
        image = ImageFactory.createDomain()
        image.id = IdGenerator.generate()
        image.propertyId = propertyId
        image.file = request.files.get("image")
        # Call Service Layer
        response = ImageService.add(image)
        return ResponseFormatter.getFormmattedServiceResponse(ImageConverter.toResource, response)

    '''Deletes an Images File and Data'''
    def remove(propertyId, imageId):
        # Authenticate
        authenticator = Authenticator(request.headers.get(HeaderKey.TOKEN)).allowAgent().allowOwnerOf(Property, "ownerId", propertyId)
        authentification = authenticator.authenticate()
        if FieldKey.ERROR in authentification:
            return ResponseFormatter.getFormattedValidatorResponse(authentification)
        # Call Service Layer
        response = ImageService.remove(propertyId, imageId)
        return ResponseFormatter.getFormmattedServiceResponse(ImageConverter.toResource, response)

    '''Updates an Images Data'''
    def update(propertyId, imageId, imageResource):
        # Authenticate
        authenticator = Authenticator(request.headers.get(HeaderKey.TOKEN)).allowAgent().allowOwnerOf(Property, "ownerId", propertyId)
        authentification = authenticator.authenticate()
        if FieldKey.ERROR in authentification:
            return ResponseFormatter.getFormattedValidatorResponse(authentification)
        # Validate Resource
        imageResourceValidation = ImageValidator.validateUpdate(imageResource)
        if FieldKey.ERROR in imageResourceValidation:
            return ResponseFormatter.getFormattedValidatorResponse(imageResourceValidation)
        # Create Domain Instance
        image = ImageConverter.toDomain(imageResource)
        image.id = imageId
        image.propertyId = propertyId
        # Call Service Layer
        response = ImageService.update(image)
        return ResponseFormatter.getFormmattedServiceResponse(ImageConverter.toResource, response)

    '''Reads an Image File'''
    def read(propertyId, imageId):
        # Authenticate
            # All Access
        # Call Service Layer
        file, type = ImageService.read(propertyId, imageId)
        return ResponseFormatter.getFileResponse(file, type)

    '''Reads all Image Data for a Property'''
    def readAll(propertyId):
        # Authenticate
            # All Access
        # Call Service Layer
        response = ImageService.readAll(propertyId)
        return ResponseFormatter.getFormmattedServiceListResponse(ImageConverter.toResource, response)

    '''Sets an Image to be the main Image for a Property'''
    def setMain(propertyId, imageId):
        # Authenticate
        authenticator = Authenticator(request.headers.get(HeaderKey.TOKEN)).allowAgent().allowOwnerOf(Property, "ownerId", propertyId)
        authentification = authenticator.authenticate()
        if FieldKey.ERROR in authentification:
            return ResponseFormatter.getFormattedValidatorResponse(authentification)
        # Call Service Layer
        response = ImageService.setMain(propertyId, imageId)
        return ResponseFormatter.getFormmattedServiceResponse(PropertyConverter.toResource, response)
