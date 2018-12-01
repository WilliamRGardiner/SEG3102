from database.Base import Base
from sqlalchemy import Column, Integer, String, ForeignKey

'''The Persisted Account Entity'''
class Account(Base):
    __tablename__ = "account"

    id = Column("id", String, primary_key=True)
    username = Column("username", String, unique=True)
    email = Column("email", String, unique=True)
    type = Column("type", String)
    firstName = Column("first_name", String)
    lastName = Column("last_name", String)
    dateOfBirth = Column("date_of_birth", String)

'''Account Types'''
class AccountType():
    AGENT = "AGENT"
    CUSTOMER = "CUSTOMER"
    OWNER = "OWNER"
