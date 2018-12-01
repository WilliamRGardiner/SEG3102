from tests.fw.TestSuite import TestSuite
from tests.tests.account.AccountTestSuite import AccountTestSuite

class MainTestSuite(TestSuite):
    def __init__(self):
        self.tests = [AccountTestSuite()]
