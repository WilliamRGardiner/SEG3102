from .AccountTestBase import AccountTestBase
from tests.facade.AgentFacade import AgentFacade
from tests.facade.CustomerFacade import CustomerFacade
from tests.facade.OwnerFacade import OwnerFacade
from tests.factory.AccountFactory import AccountFactory
from tests.fw.Assertions import Assertions
from tests.utils.External import External

class ReadTests(AccountTestBase):
    def __init__(self):
        super().__init__("Update")
        self.executor.tests = [
            self.readAgent,
            self.readCustomer,
            self.readOwner
        ]

    def readAgent(self):
        self.accountType = "agent"
        accountResource = AccountFactory().agent().toResource()
        if not self.createAccount(accountResource):
            self.assertions.append("Failed to create Agent")
        else:
            status, account = AgentFacade.read(self.adminToken, self.account['id'])
            if External.is2XX(status):
                accountResource['password'] = None
                Assertions.assertList(self.assertions, self.testTools.compare(accountResource, account))
            else:
                Assertions.assertStatusCode(self.assertions, status, External.STATUS["OK"])
                print(account)
        return self.testTools.formatAssertions(self.assertions, "readAgent")

    def readCustomer(self):
        self.accountType = "customer"
        accountResource = AccountFactory().customer().toResource()
        if not self.createAccount(accountResource):
            self.assertions.append("Failed to create Agent")
        else:
            status, account = CustomerFacade.read(self.adminToken, self.account['id'])
            if External.is2XX(status):
                accountResource['password'] = None
                Assertions.assertList(self.assertions, self.testTools.compare(accountResource, account))
            else:
                Assertions.assertStatusCode(self.assertions, status, External.STATUS["OK"])
                print(account)
        return self.testTools.formatAssertions(self.assertions, "readCustomer")

    def readOwner(self):
        self.accountType = "owner"
        accountResource = AccountFactory().owner().toResource()
        if not self.createAccount(accountResource):
            self.assertions.append("Failed to create Agent")
        else:
            status, account = OwnerFacade.read(self.adminToken, self.account['id'])
            if External.is2XX(status):
                accountResource['password'] = None
                Assertions.assertList(self.assertions, self.testTools.compare(accountResource, account))
            else:
                Assertions.assertStatusCode(self.assertions, status, External.STATUS["OK"])
                print(account)
        return self.testTools.formatAssertions(self.assertions, "readOwner")
