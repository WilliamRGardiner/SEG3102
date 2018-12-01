from database.Base import Base
from sqlalchemy import Column, Integer, String, ForeignKey

'''The Persisted Image Data Entity'''
class Image(Base):
    __tablename__ = "image"

    id = Column("id", String, primary_key=True)
    propertyId = Column("property_id", String)
    title = Column("title", String)
    description = Column("description", String)
    file = None
