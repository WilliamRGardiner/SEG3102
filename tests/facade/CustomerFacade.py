import requests
from tests.utils.External import External

class CustomerFacade():
    def create(sessionToken, customerResource):
        response = requests.post(CustomerFacade.getUrl(), json=customerResource, headers=CustomerFacade.getHeaders(sessionToken))
        return response.status_code, response.json()

    def read(sessionToken, customerId):
        response = requests.get(CustomerFacade.getUrl(customerId), headers=CustomerFacade.getHeaders(sessionToken))
        return response.status_code, response.json()

    def update(sessionToken, customerId, customerResource):
        response = requests.put(CustomerFacade.getUrl(customerId), json=customerResource, headers=CustomerFacade.getHeaders(sessionToken))
        return response.status_code, response.json()

    def delete(sessionToken, customerId):
        response = requests.delete(CustomerFacade.getUrl(customerId), headers=CustomerFacade.getHeaders(sessionToken))
        return response.status_code, response.json()

    def getUrl(customerId=None):
        url = External.getBaseUrl() + "customer"
        if customerId is not None:
            url = url + "/" + customerId
        return url

    def getHeaders(sessionToken):
        return External.getBaseHeaders(sessionToken)
