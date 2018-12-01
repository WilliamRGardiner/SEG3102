from domain.Image import Image

'''Creates an Image Data Domain Object'''
class ImageFactory():

    '''The default title'''
    DEFAULT_TITLE = "Untitled"

    '''The default description'''
    DEFAULT_DESCRIPTION = "No Description"

    '''Creates an Image Data Domain Object'''
    def createDomain():
        image = Image()
        image.title = ImageFactory.DEFAULT_TITLE
        image.description = ImageFactory.DEFAULT_DESCRIPTION
        return image
