from .ResourceValidator import ResourceValidator
from common.converter.ImageConverter import ImageField
from common.validator.BaseValidator import BaseValidator

class ImageValidator():

    FIELDS = {
        ResourceValidator.UPDATE: {
            ResourceValidator.NON_ALLOWED: [ImageField.ID, ImageField.PROPERTY]
        }
    }

    def validateUpdate(image_resource):
        errors = ResourceValidator.validate(image_resource, ImageValidator.FIELDS[ResourceValidator.UPDATE])
        return BaseValidator.getValidationMessage(errors)
