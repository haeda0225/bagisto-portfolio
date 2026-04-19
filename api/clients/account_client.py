from api.clients.base_client import BaseClient


class AccountClient(BaseClient):
    def add_customer_address(
        self,
        *,
        first_name: str,
        last_name: str,
        email: str,
        phone: str,
        address1: str,
        city: str,
        state: str,
        country: str,
        postcode: str,
        address2: str = "",
        use_for_shipping: bool = True,
        default_address: bool = True,
    ):
        mutation = """
        mutation createAddUpdateCustomerAddress($input: createAddUpdateCustomerAddressInput!) {
          createAddUpdateCustomerAddress(input: $input) {
            addUpdateCustomerAddress {
              id
              addressId
              firstName
              lastName
              email
              phone
              address1
              address2
              country
              state
              city
              postcode
              useForShipping
              defaultAddress
            }
          }
        }
        """
        payload = {
            "input": {
                "firstName": first_name,
                "lastName": last_name,
                "email": email,
                "phone": phone,
                "address1": address1,
                "address2": address2,
                "country": country,
                "state": state,
                "city": city,
                "postcode": postcode,
                "useForShipping": use_for_shipping,
                "defaultAddress": default_address,
            }
        }
        return self.execute(mutation, payload)
