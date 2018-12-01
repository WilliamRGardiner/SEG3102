from .ResourceValidator import ResourceValidator
from common.converter.RentalConverter import RentalField
from common.validator.BaseValidator import BaseValidator

class RentalValidator():
    FIELDS = {
        ResourceValidator.CREATE: {
            ResourceValidator.MANDATORY: [RentalField.CUSTOMER, RentalField.PROPERTY, RentalField.AGENT, RentalField.RENT, RentalField.START, RentalField.END],
            ResourceValidator.NON_ALLOWED: [RentalField.ID, RentalField.STATUS]
        },
        ResourceValidator.UPDATE: {
            ResourceValidator.NON_ALLOWED: [RentalField.ID, RentalField.STATUS, RentalField.CUSTOMER, RentalField.PROPERTY]
        }
    }

    def validateCreate(rental_resource):
        errors = ResourceValidator.validate(rental_resource, RentalValidator.FIELDS[ResourceValidator.CREATE])
        ResourceValidator.checkDate(errors, rental_resource, RentalField.START)
        ResourceValidator.checkDate(errors, rental_resource, RentalField.END)
        return BaseValidator.getValidationMessage(errors)

    def validateUpdate(rental_resource):
        errors = ResourceValidator.validate(rental_resource, RentalValidator.FIELDS[ResourceValidator.UPDATE])
        ResourceValidator.checkDate(errors, rental_resource, RentalField.START)
        ResourceValidator.checkDate(errors, rental_resource, RentalField.END)
        return BaseValidator.getValidationMessage(errors)
