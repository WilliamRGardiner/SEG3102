import requests
from tests.utils.External import External

class AgentFacade():
    def create(sessionToken, agentResource):
        response = requests.post(AgentFacade.getUrl(), json=agentResource, headers=AgentFacade.getHeaders(sessionToken))
        return response.status_code, response.json()

    def read(sessionToken, agentId):
        response = requests.get(AgentFacade.getUrl(agentId), headers=AgentFacade.getHeaders(sessionToken))
        return response.status_code, response.json()

    def update(sessionToken, agentId, agentResource):
        response = requests.put(AgentFacade.getUrl(agentId), json=agentResource, headers=AgentFacade.getHeaders(sessionToken))
        return response.status_code, response.json()

    def delete(sessionToken, agentId):
        response = requests.delete(AgentFacade.getUrl(agentId), headers=AgentFacade.getHeaders(sessionToken))
        return response.status_code, response.json()

    def getUrl(agentId=None):
        url = External.getBaseUrl() + "agent"
        if agentId is not None:
            url = url + "/" + agentId
        return url

    def getHeaders(sessionToken):
        return External.getBaseHeaders(sessionToken)
