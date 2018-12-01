import tests.properties

from tests.facade.AgentFacade import AgentFacade
from tests.facade.CustomerFacade import CustomerFacade
from tests.facade.OwnerFacade import OwnerFacade
from tests.facade.SessionFacade import SessionFacade
from tests.factory.SessionFactory import SessionFactory

from tests.utils.External import External
from tests.utils.TestTools import TestTools
from tests.fw.TestExecutor import TestExecutor

class AccountTestBase():
    def __init__(self, testClass):
        self.account = None
        self.adminToken = None
        self.assertions = []
        self.testTools = TestTools("Account", testClass)
        self.executor = TestExecutor(beforeAll=self.beforeAll, beforeEach=self.beforeEach, tests=[], afterEach=self.afterEach, afterAll=self.afterAll)

    def beforeAll(self):
        try:
            status, body = SessionFacade.login(SessionFactory.getLogin('admin', 'admin'))
            if not External.is2XX(status):
                return self.testTools.formatAssertion("Failed to Login as Admin", "beforeAll")
        except:
            return self.testTools.formatAssertion("Failed to Login as Admin", "beforeAll")
        self.adminToken = body['session_token']

    def beforeEach(self):
        assertions = []

    def afterEach(self):
        if self.account is not None:
            # try:
            if self.accountType == "agent":
                AgentFacade.delete(self.adminToken, self.account['id'])
            if self.accountType == "customer":
                CustomerFacade.delete(self.adminToken, self.account['id'])
            if self.accountType == "owner":
                    OwnerFacade.delete(self.adminToken, self.account['id'])
                    # except:
                # return self.testTools.formatAssertion("Failed to Delete Account", "afterEach")
            self.account = None

    def afterAll(self):
        # try:
        SessionFacade.logout(self.adminToken)
        # except:
            # return self.testTools.formatAssertion("Failed to Logout as Admin", "afterAll")
