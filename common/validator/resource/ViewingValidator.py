from .ResourceValidator import ResourceValidator
from common.converter.ViewingConverter import ViewingField
from common.validator.BaseValidator import BaseValidator

class ViewingValidator():
    FIELDS = {
        ResourceValidator.CREATE: {
            ResourceValidator.MANDATORY: [ViewingField.DATE],
            ResourceValidator.NON_ALLOWED: [ViewingField.ID, ViewingField.PROPERTY]
        },
        ResourceValidator.UPDATE: {
            ResourceValidator.NON_ALLOWED: [ViewingField.ID, ViewingField.PROPERTY]
        }
    }

    def validateCreate(viewing_resource):
        errors = ResourceValidator.validate(viewing_resource, ViewingValidator.FIELDS[ResourceValidator.CREATE])
        ResourceValidator.checkDate(errors, viewing_resource, ViewingField.DATE)
        return BaseValidator.getValidationMessage(errors)

    def validateUpdate(viewing_resource):
        errors = ResourceValidator.validate(viewing_resource, ViewingValidator.FIELDS[ResourceValidator.UPDATE])
        ResourceValidator.checkDate(errors, viewing_resource, ViewingField.DATE)
        return BaseValidator.getValidationMessage(errors)
