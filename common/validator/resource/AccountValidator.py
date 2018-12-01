from .ResourceValidator import ResourceValidator
from common.converter.AccountConverter import AccountField
from common.validator.BaseValidator import BaseValidator

class AccountValidator():

    FIELDS = {
        ResourceValidator.CREATE: {
            ResourceValidator.MANDATORY: [AccountField.USERNAME, AccountField.PASSWORD, AccountField.EMAIL],
            ResourceValidator.NON_ALLOWED: [AccountField.ID, AccountField.TYPE]
        },
        ResourceValidator.UPDATE: {
            ResourceValidator.NON_ALLOWED: [AccountField.ID, AccountField.TYPE, AccountField.USERNAME]
        }
    }

    def validateCreate(account_resource):
        errors = ResourceValidator.validate(account_resource, AccountValidator.FIELDS[ResourceValidator.CREATE])
        return BaseValidator.getValidationMessage(errors)

    def validateUpdate(account_resource):
        errors = ResourceValidator.validate(account_resource, AccountValidator.FIELDS[ResourceValidator.UPDATE])
        return BaseValidator.getValidationMessage(errors)
