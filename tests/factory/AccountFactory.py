import copy

class AccountFactory():

    FIRST_NAME = "First"
    FIRST_NAME_UPDATED = "Updated First"
    LAST_NAME = "Last"
    LAST_NAME_UPDATED = "Updated Last"
    AGENT_USERNAME = "Agent"
    CUSTOMER_USERNAME = "Customer"
    OWNER_USERNAME = "Owner"
    PASSWORD = "password"
    PASSWORD_UPDATED = "passw0rd"
    DATE_OF_BIRTH = "1990-01-01"
    DATE_OF_BIRTH_UPDATED = "1990-01-02"
    AGENT_EMAIL = "agent@company.org"
    CUSTOMER_EMAIL = "customer@company.org"
    OWNER_EMAIL = "owner@company.org"
    EMAIL_UPDATED = "updated@company.org"

    def __init__(self):
        self.resource = {
            'first_name': AccountFactory.FIRST_NAME,
            'last_name': AccountFactory.LAST_NAME,
            'username': AccountFactory.AGENT_USERNAME,
            'password': AccountFactory.PASSWORD,
            'date_of_birth': AccountFactory.DATE_OF_BIRTH,
            'email': AccountFactory.AGENT_EMAIL,
        }

    def agent(self):
        factory = copy.deepcopy(self)
        factory.resource['username'] = AccountFactory.AGENT_USERNAME
        factory.resource['email'] = AccountFactory.AGENT_EMAIL
        return factory

    def customer(self):
        factory = copy.deepcopy(self)
        factory.resource['username'] = AccountFactory.CUSTOMER_USERNAME
        factory.resource['email'] = AccountFactory.CUSTOMER_EMAIL
        return factory

    def owner(self):
        factory = copy.deepcopy(self)
        factory.resource['username'] = AccountFactory.OWNER_USERNAME
        factory.resource['email'] = AccountFactory.OWNER_EMAIL
        return factory

    def update(self):
        factory = copy.deepcopy(self)
        del factory.resource['username']
        factory.resource['first_name'] = AccountFactory.FIRST_NAME_UPDATED
        factory.resource['last_name'] = AccountFactory.LAST_NAME_UPDATED
        factory.resource['password'] = AccountFactory.PASSWORD_UPDATED
        factory.resource['date_of_birth'] = AccountFactory.DATE_OF_BIRTH_UPDATED
        factory.resource['email'] = AccountFactory.EMAIL_UPDATED
        return factory

    def toResource(self):
        return self.resource
