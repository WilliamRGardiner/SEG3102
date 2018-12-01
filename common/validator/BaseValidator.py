class BaseValidator():

    OK = "OK"

    def getValidationMessage(errorArray):
        errorResponse = {}
        if len(errorArray) > 0:
            errorResponse[ValidatorField.ERROR] = "Validation Failed"
            errorResponse[ValidatorField.ERROR_COUNT] = len(errorArray)
            errorResponse[ValidatorField.DETAILS] = errorArray
            errorResponse[ValidatorField.VALIDATION] = True
        else:
            errorResponse[ValidatorField.SUCCESS] = BaseValidator.OK
        return errorResponse

class ValidatorField():
    ERROR = "error"
    ERROR_COUNT = "error_count"
    DETAILS = "details"
    SUCCESS = "success"
    VALIDATION = "validation_error"
