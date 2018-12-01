import requests
from tests.utils.External import External

class OwnerFacade():
    def create(sessionToken, ownerResource):
        response = requests.post(OwnerFacade.getUrl(), json=ownerResource, headers=OwnerFacade.getHeaders(sessionToken))
        return response.status_code, response.json()

    def read(sessionToken, ownerId):
        response = requests.get(OwnerFacade.getUrl(ownerId), headers=OwnerFacade.getHeaders(sessionToken))
        return response.status_code, response.json()

    def update(sessionToken, ownerId, ownerResource):
        response = requests.put(OwnerFacade.getUrl(ownerId), json=ownerResource, headers=OwnerFacade.getHeaders(sessionToken))
        return response.status_code, response.json()

    def delete(sessionToken, ownerId):
        response = requests.delete(OwnerFacade.getUrl(ownerId), headers=OwnerFacade.getHeaders(sessionToken))
        return response.status_code, response.json()

    def getUrl(ownerId=None):
        url = External.getBaseUrl() + "owner"
        if ownerId is not None:
            url = url + "/" + ownerId
        return url

    def getHeaders(sessionToken):
        return External.getBaseHeaders(sessionToken)
