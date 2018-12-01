class TestSuite():
    def __init__(self, tests=[]):
        self.tests = tests

    def execute(self):
        results = []
        for test in self.tests:
            results.extend(test.execute())
        return results
