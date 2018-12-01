from common.request_constants.HttpStatus import HttpStatus
from common.request_constants.FieldKey import FieldKey

'''Creates errors that can be formatted by the ResponseFormatter'''
class Error():

    def internalError():
        return Error.getDictError("An unexpected error has occured", HttpStatus.INTERNAL_SERVER_ERROR)

    def duplicateFieldError(field, value):
        return Error.getDictError(value + " already in use for " + field, HttpStatus.BAD_REQUEST)

    def domainNotFoundError(domain, id):
        return Error.getDictError(domain + " not found with id: " + id, HttpStatus.NOT_FOUND)

    def subdomainNotFoundError(domain, subDomain, id):
        return Error.getDictError(subDomain + " not found for " + domain + " with id: " + id, HttpStatus.NOT_FOUND)

    def linkedDomainNotFoundError(domain, subDomain, id, subId):
        return Error.getDictError(subDomain + ": " + subId + " not found for " + domain + " with id: " + id, HttpStatus.NOT_FOUND)

    def getDictError(msg, status):
        return {FieldKey.ERROR: msg, FieldKey.STATUS: status}
