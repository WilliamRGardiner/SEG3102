from .AccountTestBase import AccountTestBase
from tests.facade.AgentFacade import AgentFacade
from tests.facade.CustomerFacade import CustomerFacade
from tests.facade.OwnerFacade import OwnerFacade
from tests.factory.AccountFactory import AccountFactory
from tests.fw.Assertions import Assertions
from tests.utils.External import External

class DeletionTests(AccountTestBase):
    def __init__(self):
        super().__init__("Update")
        self.executor.tests = [
            self.deleteAgent,
            self.deleteCustomer,
            self.deleteOwner
        ]

    def deleteAgent(self):
        self.accountType = "agent"
        accountResource = AccountFactory().agent().toResource()
        if not self.createAccount(accountResource):
            self.assertions.append("Failed to create Agent")
        else:
            status, account = AgentFacade.delete(self.adminToken, self.account['id'])
            if External.is2XX(status):
                accountResource['password'] = None
                Assertions.assertList(self.assertions, self.testTools.compare(accountResource, account))
                self.account = None
            else:
                Assertions.assertStatusCode(self.assertions, status, External.STATUS["OK"])
                print(account)
        return self.testTools.formatAssertions(self.assertions, "deleteAgent")

    def deleteCustomer(self):
        self.accountType = "customer"
        accountResource = AccountFactory().customer().toResource()
        if not self.createAccount(accountResource):
            self.assertions.append("Failed to create Agent")
        else:
            status, account = CustomerFacade.delete(self.adminToken, self.account['id'])
            if External.is2XX(status):
                accountResource['password'] = None
                Assertions.assertList(self.assertions, self.testTools.compare(accountResource, account))
                self.account = None
            else:
                Assertions.assertStatusCode(self.assertions, status, External.STATUS["OK"])
                print(account)
        return self.testTools.formatAssertions(self.assertions, "deleteCustomer")

    def deleteOwner(self):
        self.accountType = "owner"
        accountResource = AccountFactory().owner().toResource()
        if not self.createAccount(accountResource):
            self.assertions.append("Failed to create Agent")
        else:
            status, account = OwnerFacade.delete(self.adminToken, self.account['id'])
            if External.is2XX(status):
                accountResource['password'] = None
                Assertions.assertList(self.assertions, self.testTools.compare(accountResource, account))
                self.account = None
            else:
                Assertions.assertStatusCode(self.assertions, status, External.STATUS["OK"])
                print(account)
        return self.testTools.formatAssertions(self.assertions, "deleteOwner")
