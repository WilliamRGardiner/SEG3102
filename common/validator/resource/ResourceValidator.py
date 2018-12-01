from common.utils.Date import Date, DateFormatError

class ResourceValidator():

    CREATE = "CREATE"
    UPDATE = "UPDATE"
    MANDATORY = "MANDATORY"
    NON_ALLOWED = "NON_ALLOWED"

    def validate(resource, fields):
        errors = []
        mandatory = {}
        mandatoryFieldList = fields[ResourceValidator.MANDATORY] if ResourceValidator.MANDATORY in fields else []
        nonAllowedFieldsList = fields[ResourceValidator.NON_ALLOWED] if ResourceValidator.NON_ALLOWED in fields else []

        # Initialize Dictionary of Mandatory Fields
        for mandatoryField in mandatoryFieldList:
            mandatory[mandatoryField] = False

        # Check Each Field Probided
        for field in resource:
            if resource[field] is not None:
                if field in mandatory:
                    mandatory[field] = True
                if field in nonAllowedFieldsList:
                    errors.append(ResourceValidator.nonAllowedFieldError(field))

        # Check all mandatory fields were included
        for mandatoryField in mandatory:
            if not mandatory[mandatoryField]:
                errors.append(ResourceValidator.missingFieldError(mandatoryField))

        return errors

    def checkInt(errorArray, resource, field):
        if field in resource and field is not None:
            if not str.isdigit(resource[field]):
                errorArray.append(ResourceValidator.notAnIntegerError(field))
        return errorArray

    def checkDate(errorArray, resource, field):
        try:
            Date.toDate(resource[field])
        except DateFormatError:
            errorArray.append(ResourceValidator.notAValidDate(field))

    def missingFieldError(field):
        return {"field": field, "msg": "Field: " + field + " is mandatory."}

    def nonAllowedFieldError(field):
        return {"field": field, "msg": "Field " + field + " is not allowed in this request."}

    def notAnIntegerError(field):
        return {"field": field, "msg": "Field " + field + " must be an integer."}

    def notAValidDate(field):
        return {"field": field, "msg": "Field " + field + " must be a datetime of the format yyyy-mm-dd HH:MM."}
