from database.Base import Base
from sqlalchemy import Column, Integer, String, ForeignKey

'''The Persisted Property Entity'''
class Property(Base):
    __tablename__ = "property"

    id = Column("id", String, primary_key=True)
    ownerId = Column("owner", String)
    city = Column("city", String)
    province = Column("province", String)
    addr1 = Column("addr1", String)
    addr2 = Column("addr2", String)
    rent = Column("rent", String)
    mainImageId = Column("main_image", String)
    status = None

'''The Persisted Property Statuses Entity'''
class PropertyStatus():
    RENTED = "RENTED"
    AVAILABLE = "AVAILABLE"
    UNKNOWN = "UNKNOWN"
