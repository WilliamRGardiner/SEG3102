from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from json import dumps
from flask_jsonpify import jsonify

import properties
from common.utils.IdGenerator import IdGenerator
from common.authentification.PasswordUtility import PasswordUtility
from database.Base import Base
from database.Repository import Repository
from database.ReadOnlyAccess import ReadOnlyAccess
from domain.Account import Account, AccountType
from domain.Credential import Credential

# Router Imports
from controller.SessionController import LoginRouter, LogoutRouter
from controller.AccountController import AgentRouter, AgentIdRouter, CustomerRouter, CustomerIdRouter, OwnerRouter, OwnerIdRouter
from controller.PropertyController import PropertyRouter, PropertyIdRouter, PropertySimpleRouter, PropertyHistoryRouter, PropertySearchRouter
from controller.ImageController import ImageRouter, ImageIdRouter, ImageMainRouter
from controller.ViewingController import ViewingRouter, ViewingIdRouter
from controller.RentalController import RentalRouter, RentalIdRouter, RentalConfirmRouter, RentalDenyRouter, RentalCancelRouter, RentalQueryRouter, RentalCustomerRouter

# Create DB Connection
Repository.engine = create_engine(properties.database_type+'://'+properties.database_username+':'+properties.database_password+'@'+properties.database_host+'/'+properties.database_name, echo=properties.database_echo)
Repository.Session = sessionmaker(bind=Repository.engine)

# Flask Setup
app = Flask(__name__)
api = Api(app)

# Initialize / Update Repository
Base.metadata.create_all(bind=Repository.engine)

# Create Admin Agent if no Agent Exists
if len(ReadOnlyAccess.getEntityListCopy(Account, {"type": AccountType.AGENT})) == 0:
    session = Repository.Session()
    # Create the Account object
    account = Account()
    account.id = IdGenerator.generate()
    account.username = properties.admin_username
    account.email = properties.admin_email
    account.type = AccountType.AGENT
    session.add(account)

    # Create the Credential Object
    credential = Credential()
    credential.id = account.id
    credential.password = PasswordUtility.getHashedPassword(properties.admin_password)
    session.add(credential)
    session.commit()

# API URL Mappings
api.add_resource(LoginRouter, '/login')
api.add_resource(LogoutRouter, '/logout')
api.add_resource(AgentRouter, '/agent')
api.add_resource(AgentIdRouter, '/agent/<agentId>')
api.add_resource(CustomerRouter, '/customer')
api.add_resource(CustomerIdRouter, '/customer/<customerId>')
api.add_resource(OwnerRouter, '/owner')
api.add_resource(OwnerIdRouter, '/owner/<ownerId>')
api.add_resource(PropertyRouter, '/owner/<ownerId>/property')
api.add_resource(PropertyIdRouter, '/owner/<ownerId>/property/<propertyId>')
api.add_resource(PropertySimpleRouter, '/property/<propertyId>')
api.add_resource(PropertySearchRouter, '/property/search')
api.add_resource(PropertyHistoryRouter, '/owner/{ownerId}/history')
api.add_resource(ImageRouter, '/property/<propertyId>/image')
api.add_resource(ImageIdRouter, '/property/<propertyId>/image/<imageId>')
api.add_resource(ImageMainRouter, '/property/<propertyId>/image/<imageId>/main')
api.add_resource(ViewingRouter, '/customer/<customerId>/viewing')
api.add_resource(ViewingIdRouter, '/customer/<customerId>/viewing/<viewingId>')
api.add_resource(RentalRouter, '/rental')
api.add_resource(RentalIdRouter, '/rental/<rentalId>')
api.add_resource(RentalConfirmRouter, '/rental/<rentalId>/confirm')
api.add_resource(RentalDenyRouter, '/rental/<rentalId>/deny')
api.add_resource(RentalCancelRouter, '/rental/<rentalId>/cancel')
api.add_resource(RentalQueryRouter, '/rental/query')
api.add_resource(RentalCustomerRouter, '/rental/customer/<customerId>')

# Run on Port
if __name__ == '__main__':
     app.run(port=properties.app_port)
