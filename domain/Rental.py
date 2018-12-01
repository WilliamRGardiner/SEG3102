from database.Base import Base
from sqlalchemy import Column, Integer, String, ForeignKey

'''The Persisted Rental Entity'''
class Rental(Base):
    __tablename__ = "rental"

    id = Column("id", String, primary_key=True)
    property = Column("property", String)
    customer = Column("customer", String)
    agent = Column("agent", String)
    rent = Column("rent", String)
    start = Column("start_date", String)
    end = Column("end_date", String)
    status = Column("status", String)

'''The Rental Statuses'''
class RentalStatus():
    PROPOSED = "PROPOSED"
    CONFIRMED = "CONFIRMED"
    DENIED = "DENIED"
    CANCELLED = "CANCELLED"
