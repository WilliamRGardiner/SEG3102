import requests

from tests.utils.External import External

class SessionFacade():
    def login(resource):
        response = requests.put(SessionFacade.getUrl("login"), json=resource)
        return response.status_code, response.json()

    def logout(sessionToken):
        response = requests.put(SessionFacade.getUrl("logout"), headers=SessionFacade.getHeaders(sessionToken))
        return response.status_code, response.json()

    def getUrl(action):
        url = External.getBaseUrl() + action
        return url

    def getHeaders(sessionToken):
        return External.getBaseHeaders(sessionToken)
