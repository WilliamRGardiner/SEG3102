from common.utils.Date import Date
from domain.Viewing import Viewing

'''Converts Viewings'''
class ViewingConverter():

    '''Creates the Domain Object used internally'''
    def toDomain(viewingResource):
        viewing = Viewing()
        viewing.id = viewingResource[ViewingField.ID] if ViewingField.ID in viewingResource else None
        viewing.date = Date.formatDate(viewingResource[ViewingField.DATE]) if ViewingField.DATE in viewingResource else None
        viewing.comment = viewingResource[ViewingField.COMMENT] if ViewingField.COMMENT in viewingResource else None
        return viewing

    '''Creates the Resource returned to the Caller'''
    def toResource(viewing):
        viewingResource = {
            ViewingField.ID: viewing.id,
            ViewingField.CUSTOMER: viewing.customerId,
            ViewingField.PROPERTY: viewing.propertyId,
            ViewingField.DATE: viewing.date,
            ViewingField.COMMENT: viewing.comment
        }
        return viewingResource

'''The known JSON fields'''
class ViewingField():
        ID = "id"
        CUSTOMER = "customer_id"
        PROPERTY = "property_id"
        DATE = "date"
        COMMENT = "comment"
