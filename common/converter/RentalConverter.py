from common.utils.Date import Date
from domain.Rental import Rental

'''Converts Rentals'''
class RentalConverter():

    '''Creates the Domain Object used internally'''
    def toDomain(rentalResource):
        rental = Rental()
        rental.id = rentalResource[RentalField.ID] if RentalField.ID in rentalResource else None
        rental.customer = rentalResource[RentalField.CUSTOMER] if RentalField.CUSTOMER in rentalResource else None
        rental.property = rentalResource[RentalField.PROPERTY] if RentalField.PROPERTY in rentalResource else None
        rental.agent = rentalResource[RentalField.AGENT] if RentalField.AGENT in rentalResource else None
        rental.rent = rentalResource[RentalField.RENT] if RentalField.RENT in rentalResource else None
        rental.start = Date.formatDate(rentalResource[RentalField.START]) if RentalField.START in rentalResource else None
        rental.end = Date.formatDate(rentalResource[RentalField.END]) if RentalField.END in rentalResource else None
        rental.status = rentalResource[RentalField.STATUS] if RentalField.STATUS in rentalResource else None
        return rental

    '''Creates the Resource returned to the Caller'''
    def toResource(rental):
        rentalResource = {
            RentalField.ID: rental.id,
            RentalField.CUSTOMER: rental.customer,
            RentalField.PROPERTY: rental.property,
            RentalField.AGENT: rental.agent,
            RentalField.RENT: rental.rent,
            RentalField.START: rental.start,
            RentalField.END: rental.end,
            RentalField.STATUS: rental.status
        }
        return rentalResource

'''The known JSON fields'''
class RentalField():
    ID = "id"
    CUSTOMER = "customer"
    PROPERTY = "property"
    AGENT = "agent"
    RENT = "amount"
    START = "start"
    END = "end"
    STATUS = "status"
