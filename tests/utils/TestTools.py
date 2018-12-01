class TestTools():
    def __init__(self, testSuite, testClass):
        self.testSuite = testSuite
        self.testClass = testClass

    def formatAssertions(self, assertions, testName):
        return [self.formatAssertion(assertion, testName) for assertion in assertions]

    def formatAssertion(self, assertion, testName):
        return self.testSuite + " - " + self.testClass + "." + testName + ": " + assertion

    def compare(self, expected, received):
        assertions = []
        for k in expected:
            if expected[k] is not None:
                if k in received:
                    if received[k] is None:
                        received[k] = "None"
                    if not received[k] == expected[k]:
                        assertions.append("Unexpected value for " + k + ", expected " + expected[k] + " received " + received[k])
                else:
                    assertions.append("Missing key " + k + " in response.")
        return assertions
