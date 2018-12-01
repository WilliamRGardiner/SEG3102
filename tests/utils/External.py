import properties

class External():

    STATUS = {
        "OK": 200,
        "CREATED": 201
    }

    def is2XX(statusCode):
        firstDigit = int(statusCode) // 100
        return firstDigit == 2

    def getBaseUrl():
        return "http://localhost:" + properties.app_port + "/"

    def getBaseHeaders(sessionToken):
        return {
            'X-TOKEN': sessionToken
        }
