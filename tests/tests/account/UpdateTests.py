from .AccountTestBase import AccountTestBase
from tests.facade.AgentFacade import AgentFacade
from tests.facade.CustomerFacade import CustomerFacade
from tests.facade.OwnerFacade import OwnerFacade
from tests.factory.AccountFactory import AccountFactory
from tests.fw.Assertions import Assertions
from tests.utils.External import External

class UpdateTests(AccountTestBase):
    def __init__(self):
        super().__init__("Update")
        self.executor.tests = [
            self.updateAgent,
            self.updateCustomer,
            self.updateOwner
        ]

    def updateAgent(self):
        self.accountType = "agent"
        accountFactory = AccountFactory().agent()
        if not self.createAccount(accountFactory.toResource()):
            self.assertions.append("Failed to create Agent")
        else:
            accountResource = accountFactory.update().toResource()
            status, account = AgentFacade.update(self.adminToken, self.account['id'], accountResource)
            if External.is2XX(status):
                accountResource['password'] = None
                Assertions.assertList(self.assertions, self.testTools.compare(accountResource, account))
            else:
                Assertions.assertStatusCode(self.assertions, status, External.STATUS["OK"])
                print(account)
        return self.testTools.formatAssertions(self.assertions, "updateAgent")

    def updateCustomer(self):
        self.accountType = "customer"
        accountFactory = AccountFactory().customer()
        if not self.createAccount(accountFactory.toResource()):
            self.assertions.append("Failed to create Agent")
        else:
            accountResource = accountFactory.update().toResource()
            status, account = CustomerFacade.update(self.adminToken, self.account['id'], accountResource)
            if External.is2XX(status):
                accountResource['password'] = None
                Assertions.assertList(self.assertions, self.testTools.compare(accountResource, account))
            else:
                Assertions.assertStatusCode(self.assertions, status, External.STATUS["OK"])
                print(account)
        return self.testTools.formatAssertions(self.assertions, "updateCustomer")

    def updateOwner(self):
        self.accountType = "owner"
        accountFactory = AccountFactory().owner()
        if not self.createAccount(accountFactory.toResource()):
            self.assertions.append("Failed to create Agent")
        else:
            accountResource = accountFactory.update().toResource()
            status, account = OwnerFacade.update(self.adminToken, self.account['id'], accountResource)
            if External.is2XX(status):
                accountResource['password'] = None
                Assertions.assertList(self.assertions, self.testTools.compare(accountResource, account))
            else:
                Assertions.assertStatusCode(self.assertions, status, External.STATUS["OK"])
                print(account)
        return self.testTools.formatAssertions(self.assertions, "updateOwner")
