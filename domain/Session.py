from database.Base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, LargeBinary

'''The Persisted Session Entity'''
class Session(Base):
    __tablename__ = "session"

    id = Column("token", String, primary_key=True)
    username = Column("username", String, unique=True)
    lastUsed = Column("last_used", String)
