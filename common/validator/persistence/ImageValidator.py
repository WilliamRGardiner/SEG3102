from .PersistenceValidator import PersistenceValidator
from domain.Image import Image
from domain.Property import Property
from common.validator.BaseValidator import BaseValidator
from database.ReadOnlyAccess import ReadOnlyAccess

class ImageValidator():
    def validateCreate(image):
        errors = []
        return BaseValidator.getValidationMessage(ImageValidator.checkUniqueness(errors, image))

    def validateRead(propertyId, imageId):
        errors = []
        if not PersistenceValidator.checkExists(Image, imageId):
            errors.append(PersistenceValidator.entityDoesNotExist("Image", "id", imageId))
        if not PersistenceValidator.checkExists(Property, propertyId):
            errors.append(PersistenceValidator.entityDoesNotExist("Property", "id", propertyId))
        if not ReadOnlyAccess.getEntityCopy(Image, imageId).propertyId == propertyId:
            errors.append(linkedDomainNotFoundError("Property", "Image", propertyId, imageId))
        return BaseValidator.getValidationMessage(errors)

    def validateUpdate(image):
        errors = []
        if PersistenceValidator.checkExists(Image, image.id):
            original = ReadOnlyAccess.getEntityCopy(Image, image.id)
        else:
            original = Image()
            errors.append(PersistenceValidator.entityDoesNotExist("Image", "id", image.id))
        return BaseValidator.getValidationMessage(ImageValidator.checkUniqueness(errors, image, original))

    def validateDelete(propertyId, imageId):
        return ImageValidator.validateRead(propertyId, imageId)

    def validateReadAll(propertyId):
        errors = []
        if not PersistenceValidator.checkExists(Property, propertyId):
            errors.append(PersistenceValidator.entityDoesNotExist("Property", "id", propertyId))
        return BaseValidator.getValidationMessage(errors)

    def validateSetMain(propertyId, imageId):
        return ImageValidator.validateRead(propertyId, imageId)

    def checkUniqueness(errors, image, original=Image()):
        return errors
