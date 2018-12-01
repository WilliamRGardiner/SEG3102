from .AccountTestBase import AccountTestBase
from tests.facade.AgentFacade import AgentFacade
from tests.facade.CustomerFacade import CustomerFacade
from tests.facade.OwnerFacade import OwnerFacade
from tests.factory.AccountFactory import AccountFactory
from tests.fw.Assertions import Assertions
from tests.utils.External import External

class CreationTests(AccountTestBase):
    def __init__(self):
        super().__init__("Creation")
        self.executor.tests = [
            self.createAgent,
            self.createCustomer,
            self.createOwner
        ]

    def createAgent(self):
        accountResource = AccountFactory().agent().toResource()
        status, body = AgentFacade.create(self.adminToken, accountResource)
        Assertions.assertStatusCode(self.assertions, status, External.STATUS["OK"])
        if External.is2XX(status):
            self.account = body
            self.accountType = "agent"
            accountResource['password'] = None
            Assertions.assertList(self.assertions, self.testTools.compare(accountResource, self.account))
        else:
            print(body)
        return self.testTools.formatAssertions(self.assertions, "createAgent")

    def createCustomer(self):
        accountResource = AccountFactory().customer().toResource()
        status, body = CustomerFacade.create(self.adminToken, accountResource)
        Assertions.assertStatusCode(self.assertions, status, External.STATUS["OK"])
        if External.is2XX(status):
            self.account = body
            self.accountType = "customer"
            accountResource['password'] = None
            Assertions.assertList(self.assertions, self.testTools.compare(accountResource, self.account))
        else:
            print(body)
        return self.testTools.formatAssertions(self.assertions, "createCustomer")

    def createOwner(self):
        accountResource = AccountFactory().owner().toResource()
        status, body = OwnerFacade.create(self.adminToken, accountResource)
        Assertions.assertStatusCode(self.assertions, status, External.STATUS["OK"])
        if External.is2XX(status):
            self.account = body
            self.accountType = "owner"
            accountResource['password'] = None
            Assertions.assertList(self.assertions, self.testTools.compare(accountResource, self.account))
        else:
            print(body)
        return self.testTools.formatAssertions(self.assertions, "createOwner")
