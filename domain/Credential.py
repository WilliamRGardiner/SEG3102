from database.Base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, LargeBinary

'''The Persisted Account Entity'''
class Credential(Base):
    __tablename__ = "credential"

    id = Column("account_id", String, primary_key=True)
    password = Column("password", LargeBinary, unique=True)
