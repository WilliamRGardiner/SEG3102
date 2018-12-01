from tests.fw.TestSuite import TestSuite
from .CreationTests import CreationTests
from .UpdateTests import UpdateTests
from .DeletionTests import DeletionTests
from .ReadTests import ReadTests

class AccountTestSuite(TestSuite):
    def __init__(self):
        super().__init__()
        self.tests.append(CreationTests().executor)
        self.tests.append(UpdateTests().executor)
        self.tests.append(DeletionTests().executor)
        self.tests.append(ReadTests().executor)
