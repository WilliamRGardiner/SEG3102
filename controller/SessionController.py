from flask import Flask, request
from flask_restful import Resource, Api
from json import loads

from common.converter.SessionConverter import SessionConverter
from common.converter.AccountConverter import AccountConverter, AccountField
from common.factory.SessionFactory import SessionFactory
from common.request_constants.HttpStatus import HttpStatus
from common.request_constants.FieldKey import FieldKey
from common.request_constants.HeaderKey import HeaderKey
from common.utils.ResponseFormatter import ResponseFormatter
from common.utils.IdGenerator import IdGenerator
from common.validator.resource.AccountValidator import AccountValidator

from domain.Session import Session
from service.SessionService import SessionService

'''Routes incoming calls to the SessionController'''
class LoginRouter(Resource):
    def put(self):
        return SessionController.login(loads(request.data))

'''Routes incoming calls to the SessionController'''
class LogoutRouter(Resource):
    def put(self):
        return SessionController.logout()

'''
Authenticates Caller,
calidates incoming resources and converts them to Domain Objects,
calls the Service layer to manage the persistence operations,
returns the response from the Service layer.
'''
class SessionController:

    '''Creates a Session'''
    def login(resource):
        session = SessionFactory.createDomain(resource[AccountField.USERNAME])
        response = SessionService.login(session, resource[AccountField.PASSWORD])
        return ResponseFormatter.getFormmattedServiceResponse(SessionConverter.toResource, response)

    '''Deletes a Session'''
    def logout():
        response = SessionService.logout(request.headers.get(HeaderKey.TOKEN))
        return ResponseFormatter.getFormmattedServiceResponse(SessionConverter.toResource, response)
