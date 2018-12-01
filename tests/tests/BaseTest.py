import tests.properties

from tests.facade.SessionFacade import SessionFacade
from tests.factory.SessionFactory import SessionFactory

from tests.utils.TestTools import TestTools
from tests.fw.TestExecutor import TestExecutor

from tests.utils.External import External

class BaseTest():
    def __init__(self, testSuite, testClass):
        self.adminToken = None
        self.assertions = []
        self.testTools = TestTools(testSuite, testClass)
        self.executor = TestExecutor(
            name=testSuite,
            beforeAll=self.beforeAll,
            beforeEach=self.beforeEach,
            tests=[],
            afterEach=self.afterEach,
            afterAll=self.afterAll
        )

    def beforeAll(self):
        try:
            status, body = SessionFacade.login(SessionFactory.getLogin('admin', 'admin'))
            if not External.is2XX(status):
                return self.testTools.formatAssertion("Failed to Login as Admin", "beforeAll")
        except:
            return self.testTools.formatAssertion("Failed to Login as Admin", "beforeAll")
        self.adminToken = body['session_token']

    def beforeEach(self):
        self.assertions = []

    def beforeAll(self):
        pass

    def afterAll(self):
        try:
            SessionFacade.logout(self.adminToken)
        except:
            return self.testTools.formatAssertion("Failed to Logout as Admin", "afterAll")
