from domain.Image import Image

'''Converts Image Data'''
class ImageConverter():

    '''Creates the Domain Object used internally'''
    def toDomain(imageResource):
        image = Image()
        image.id = imageResource[ImageField.ID] if ImageField.ID in imageResource else None
        image.title = imageResource[ImageField.TITLE] if ImageField.TITLE in imageResource else None
        image.propertyId = imageResource[ImageField.PROPERTY] if ImageField.PROPERTY in imageResource else None
        image.description = imageResource[ImageField.DESCRIPTION] if ImageField.DESCRIPTION in imageResource else None
        return image

    '''Creates the Resource returned to the Caller'''
    def toResource(image):
        imageResource = {
            ImageField.ID: image.id,
            ImageField.TITLE: image.title,
            ImageField.PROPERTY: image.propertyId,
            ImageField.DESCRIPTION: image.description
        }
        return imageResource

'''The known JSON fields'''
class ImageField():
        ID = "id"
        TITLE = "title"
        PROPERTY = "property_id"
        DESCRIPTION = "description"
