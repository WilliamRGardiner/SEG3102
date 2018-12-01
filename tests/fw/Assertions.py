class Assertions():
    def assertStatusCode(assertions, received, expected):
        if not received == expected:
            assertions.append("Status Code " + str(received) + " received, expected " + str(expected))

    def assertList(assertions, newList):
        assertions.extend(newList)
