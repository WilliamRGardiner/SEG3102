import os
import copy
from flask import send_file

from database.Repository import Repository
from database.ReadOnlyAccess import ReadOnlyAccess

from common.request_constants.HttpStatus import HttpStatus
from common.request_constants.FieldKey import FieldKey
from common.Error import Error
from common.utils.FileSystemUtil import FileSystemUtil
from common.validator.persistence.ImageValidator import ImageValidator

from domain.Image import Image
from domain.Property import Property
from service.PropertyService import PropertyService

from task.TaskProcessor import TaskProcessor
from task.repository.SaveNewEntityTask import SaveNewEntityTask
from task.repository.UpdateEntityTask import UpdateEntityTask
from task.repository.DeleteEntityTask import DeleteEntityTask
from task.repository.DetachForeignKeyTask import DetachForeignKeyTask
from task.file_system.SaveToFileSystemTask import SaveToFileSystemTask
from task.file_system.RemoveFromFileSystemTask import RemoveFromFileSystemTask
from task.file_system.FlushDirectoryTask import FlushDirectoryTask

'''
Validates Images agains the persistence layer,
reads Images from the persistence layer,
and performs operations on Images via Tasks
'''
class ImageService():
    def add(image):
        # Validate in persistence level
        validatorResponse = ImageValidator.validateCreate(image)
        if FieldKey.ERROR in validatorResponse:
            return validatorResponse
        # Get Property Info
        property = ReadOnlyAccess.getEntityCopy(Property, image.propertyId)
        # Create and process Tasks
        processor = TaskProcessor()
        processor.add(SaveToFileSystemTask("images", property.ownerId, image.id, image.file, "jpg"))
        processor.add(SaveNewEntityTask(image))
        processor.process()
        # Return Result
        return {FieldKey.SUCCESS: image}

    def remove(propertyId, imageId):
        # Validate in persistence level
        validatorResponse = ImageValidator.validateDelete(propertyId, imageId)
        if FieldKey.ERROR in validatorResponse:
            return validatorResponse
        # Get return copy, before delete
        image = ReadOnlyAccess.getEntityCopy(Image, imageId)
        property = ReadOnlyAccess.getEntityCopy(Property, propertyId)
        # Create and process Tasks
        processor = TaskProcessor()
        processor.add(RemoveFromFileSystemTask("images", property.ownerId, imageId, "jpg"))
        processor.add(DetachForeignKeyTask(Property, "mainImageId", imageId))
        processor.add(DeleteEntityTask(Image, imageId))
        processor.add(FlushDirectoryTask("images", []))
        processor.process()
        # Return Result
        return {FieldKey.SUCCESS: image}

    def update(updatedImage):
        # Validate in persistence level
        validatorResponse = ImageValidator.validateUpdate(updatedImage)
        if FieldKey.ERROR in validatorResponse:
            return validatorResponse
        # Create and process Tasks
        processor = TaskProcessor()
        processor.add(UpdateEntityTask(Image, ImageService.mergeImages, updatedImage))
        processor.process()
        # Return Result
        image = ReadOnlyAccess.getEntityCopy(Image, updatedImage.id)
        return {FieldKey.SUCCESS: image}

    def read(propertyId, imageId):
        # Validate in persistence level
        validatorResponse = ImageValidator.validateRead(propertyId, imageId)
        if FieldKey.ERROR in validatorResponse:
            return validatorResponse
        # Create and process Tasks
        property = ReadOnlyAccess.getEntityCopy(Property, propertyId)
        # Return Result
        path = FileSystemUtil.getPath("images", property.ownerId)
        return os.path.join(path, imageId + ".jpg"), 'image/jpg'

    def readAll(propertyId):
        # Validate in persistence level
        validatorResponse = ImageValidator.validateReadAll(propertyId)
        if FieldKey.ERROR in validatorResponse:
            return validatorResponse
        # Read Entities
        searchFilter = {"propertyId": propertyId}
        imageList = ReadOnlyAccess.getEntityListCopy(Image, {"propertyId": propertyId})
        # Return Result
        return {FieldKey.SUCCESS: imageList}

    def setMain(propertyId, imageId):
        # Validate in persistence level
        validatorResponse = ImageValidator.validateSetMain(propertyId, imageId)
        if FieldKey.ERROR in validatorResponse:
            return validatorResponse
        # Create Updated Property
        updatedProperty = Property()
        updatedProperty.id = propertyId
        updatedProperty.mainImageId = imageId
        # Create and process Tasks
        processor = TaskProcessor()
        processor.add(UpdateEntityTask(Property, PropertyService.mergeProperties, updatedProperty))
        processor.process()

        property = ReadOnlyAccess.getEntityCopy(Property, propertyId)
        return {FieldKey.SUCCESS: property}

    def mergeImages(original, new):
        original.title = new.title if new.title is not None else original.title
        original.description = new.description if new.description is not None else original.description
        return original
