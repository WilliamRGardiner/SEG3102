from domain.Property import Property, PropertyStatus

'''Converts Properties'''
class PropertyConverter():

    '''Creates the Domain Object used internally'''
    def toDomain(propertyResource):
        property = Property()
        property.id = propertyResource[PropertyField.ID] if PropertyField.ID in propertyResource else None
        property.ownerId = propertyResource[PropertyField.OWNER] if PropertyField.OWNER in propertyResource else None
        property.city = propertyResource[PropertyField.CITY] if PropertyField.CITY in propertyResource else None
        property.province = propertyResource[PropertyField.PROVINCE] if PropertyField.PROVINCE in propertyResource else None
        property.addr1 = propertyResource[PropertyField.ADDR1] if PropertyField.ADDR1 in propertyResource else None
        property.addr2 = propertyResource[PropertyField.ADDR2] if PropertyField.ADDR2 in propertyResource else None
        property.rent = propertyResource[PropertyField.RENT] if PropertyField.RENT in propertyResource else None
        property.mainImageId = propertyResource[PropertyField.MAIN_IMAGE] if PropertyField.MAIN_IMAGE in propertyResource else None
        return property

    '''Creates the Resource returned to the Caller'''
    def toResource(property):
        propertyResource = {
            PropertyField.ID: property.id,
            PropertyField.OWNER: property.ownerId,
            PropertyField.CITY: property.city,
            PropertyField.PROVINCE: property.province,
            PropertyField.ADDR1: property.addr1,
            PropertyField.ADDR2: property.addr2,
            PropertyField.RENT: property.rent,
            PropertyField.MAIN_IMAGE: property.mainImageId,
            PropertyField.STATUS: PropertyStatus.UNKNOWN
        }
        return propertyResource

'''The known JSON fields'''
class PropertyField():
        ID = "id"
        OWNER = "owner_id"
        CITY = "city"
        PROVINCE = "province"
        ADDR1 = "addr1"
        ADDR2 = "addr2"
        RENT = "rent"
        STATUS = "status"
        MAIN_IMAGE = "main_image_id"
