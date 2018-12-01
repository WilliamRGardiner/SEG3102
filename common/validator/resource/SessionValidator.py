from .ResourceValidator import ResourceValidator
from common.converter.SessionConverter import SessionField
from common.validator.BaseValidator import BaseValidator

class SessionValidator():

    FIELDS = {
        ResourceValidator.CREATE: {
            ResourceValidator.MANDATORY: [AccountField.USERNAME, AccountField.PASSWORD]
        }
    }

    def validateCreate(session_resource):
        errors = ResourceValidator.validate(session_resource, SessionValidator.FIELDS[ResourceValidator.CREATE])
        return BaseValidator.getValidationMessage(errors)
