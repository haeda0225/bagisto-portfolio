from api.clients.base_client import BaseClient


class AuthClient(BaseClient):
    def register_customer(
        self,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
        phone: str,
    ):
        mutation = """
        mutation registerCustomer($input: createCustomerInput!) {
          createCustomer(input: $input) {
            customer {
              id
              firstName
              lastName
              email
              phone
              status
              subscribedToNewsLetter
              isVerified
              isSuspended
              token
              apiToken
            }
          }
        }
        """
        payload = {
            "input": {
                "firstName": first_name,
                "lastName": last_name,
                "email": email,
                "password": password,
                "phone": phone,
                "status": "1",
                "subscribedToNewsLetter": False,
                "isVerified": "0",
                "isSuspended": "0",
            }
        }
        return self.execute(mutation, payload)

    def login_customer(self, email: str, password: str):
        mutation = """
        mutation loginCustomer($input: createCustomerLoginInput!) {
          createCustomerLogin(input: $input) {
            customerLogin {
              id
              token
              apiToken
              success
              message
            }
          }
        }
        """
        return self.execute(
            mutation,
            {"input": {"email": email, "password": password}},
        )

    def profile(self):
        query = """
        query getCustomer {
          customer {
            id
            firstName
            lastName
            email
            phone
          }
        }
        """
        return self.execute(query)

    def orders(self):
        query = """
        query getCustomerOrders($first: Int) {
          customerOrders(first: $first) {
            totalCount
            edges {
              node {
                id
                _id
                incrementId
                status
                customerEmail
              }
            }
          }
        }
        """
        return self.execute(query, {"first": 10})
