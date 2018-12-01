from database.Base import Base
from sqlalchemy import Column, Integer, String, ForeignKey

'''The Persisted Viewing Entity'''
class Viewing(Base):
    __tablename__ = "viewing"

    id = Column("id", String, primary_key=True)
    propertyId = Column("property", String)
    customerId = Column("customer", String)
    date = Column("date", String)
    comment = Column("comment", String)
