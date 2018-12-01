from tests.tests.MainTestSuite import MainTestSuite

mainTestSuite = MainTestSuite()
for error in mainTestSuite.execute():
    print(error)
