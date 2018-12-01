from flask import send_file
from flask_jsonpify import jsonify
from common.request_constants.FieldKey import FieldKey
from common.request_constants.HttpStatus import HttpStatus
from common.validator.BaseValidator import ValidatorField

'''Formats the response for the caller'''
class ResponseFormatter():

    '''Formats a single item response from the service'''
    def getFormmattedServiceResponse(fConverter, response, removeNone=True):
        if FieldKey.ERROR in response:
            if ValidatorField.VALIDATION in response:
                return ResponseFormatter.getFormattedValidatorResponse(response)
            return ResponseFormatter.getJsonResponse({FieldKey.ERROR: response[FieldKey.ERROR]}, response[FieldKey.STATUS])
        return ResponseFormatter.getJsonResponse(ResponseFormatter.removeNone(fConverter(response[FieldKey.SUCCESS]), removeNone))

    '''Formats a list response from the service'''
    def getFormmattedServiceListResponse(fConverter, response, removeNone=True):
        if FieldKey.ERROR in response:
            if ValidatorField.VALIDATION in response:
                return ResponseFormatter.getFormattedValidatorResponse(response)
            return ResponseFormatter.getJsonResponse({FieldKey.ERROR: response[FieldKey.ERROR]}, response[FieldKey.STATUS])
        return ResponseFormatter.getJsonResponse([ResponseFormatter.removeNone(fConverter(property), removeNone) for property in response[FieldKey.SUCCESS]])

    '''Removes all None values fro a dictionary. If removeNone is False, it does nothing'''
    def removeNone(dict, removeNone=True):
        if removeNone:
            newDict = {}
            for k in dict:
                if dict[k] is not None:
                    newDict[k] = dict[k]
        else:
            newDict = dict
        return newDict

    '''Formats the Response from a Resource Validator'''
    def getFormattedValidatorResponse(resourceValidation):
        response = {}
        for k in resourceValidation:
            if not k == ValidatorField.VALIDATION:
                response[k] = resourceValidation[k]
        return ResponseFormatter.getJsonResponse(response, HttpStatus.BAD_REQUEST)

    '''Given the response body, serializes it to JSON and adds the response status'''
    def getJsonResponse(body, status=200):
        response = jsonify(body)
        response.status_code = status
        return response

    '''Creates a response for sending a file'''
    def getFileResponse(file, type):
        return send_file(file, mimetype=type)
