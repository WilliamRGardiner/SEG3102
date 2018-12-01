class TestExecutor():

    def __init__(self, beforeAll=None, beforeEach=None, tests=[], afterEach=None, afterAll=None, name="Unknown"):
        self.beforeAll = beforeAll
        self.beforeEach = beforeEach
        self.tests = tests
        self.afterEach = afterEach
        self.afterAll = afterAll
        self.name = name

    def execute(self):
        results = {
            'setup': None,
            'tests': [],
            'teardown': None
        }

        if self.beforeAll is not None:
            result = self.beforeAll()
            if result is not None:
                results['setup'] = result

        if results['setup'] is None:
            for test in self.tests:
                testName = test.__name__
                isErr = False
                errors = []
                print("Running: " + testName, end =" ")
                try:
                    if self.beforeEach is not None:
                        result = self.beforeEach()
                        if result is not None:
                            errors.append(result)

                    result = test()
                    if not len(result) == 0:
                        errors.extend(result)
                except:
                    isErr = True
                    print("Error")
                finally:
                    if self.afterEach is not None:
                        result = self.afterEach()
                        if result is not None:
                            errors.append(result)

                results['tests'].append({'name': testName, 'errors': errors, 'err': isErr})

                if len(errors) == 0:
                    print("Passed")
                else:
                    print("Failed")

        if self.afterAll is not None:
            result = self.afterAll()
            if result is not None:
                results['teardown'] = result

        return results
