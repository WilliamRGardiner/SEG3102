from .ResourceValidator import ResourceValidator
from common.converter.PropertyConverter import PropertyField
from common.validator.BaseValidator import BaseValidator

class PropertyValidator():
    FIELDS = {
        ResourceValidator.CREATE: {
            ResourceValidator.MANDATORY: [PropertyField.CITY, PropertyField.PROVINCE, PropertyField.RENT],
            ResourceValidator.NON_ALLOWED: [PropertyField.ID, PropertyField.OWNER]
        },
        ResourceValidator.UPDATE: {
            ResourceValidator.NON_ALLOWED: [PropertyField.ID, PropertyField.OWNER]
        }
    }

    def validateCreate(property_resource):
        errors = ResourceValidator.validate(property_resource, PropertyValidator.FIELDS[ResourceValidator.CREATE])
        ResourceValidator.checkInt(errors, property_resource, PropertyField.RENT)
        return BaseValidator.getValidationMessage(errors)

    def validateUpdate(property_resource):
        errors = ResourceValidator.validate(property_resource, PropertyValidator.FIELDS[ResourceValidator.UPDATE])
        ResourceValidator.checkInt(errors, property_resource, PropertyField.RENT)
        return BaseValidator.getValidationMessage(errors)
