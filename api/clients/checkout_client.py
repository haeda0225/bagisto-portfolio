from api.clients.base_client import BaseClient


class CheckoutClient(BaseClient):
    def save_checkout_address(
        self,
        *,
        first_name: str,
        last_name: str,
        email: str,
        phone: str,
        address: str,
        city: str,
        country: str,
        state: str,
        postcode: str,
        company_name: str = "",
        use_for_shipping: bool = True,
    ):
        mutation = """
        mutation createCheckoutAddress($input: createCheckoutAddressInput!) {
          createCheckoutAddress(input: $input) {
            checkoutAddress {
              success
              message
              id
              cartToken
            }
          }
        }
        """
        payload = {
            "input": {
                "billingFirstName": first_name,
                "billingLastName": last_name,
                "billingEmail": email,
                "billingCompanyName": company_name,
                "billingAddress": address,
                "billingCity": city,
                "billingCountry": country,
                "billingState": state,
                "billingPostcode": postcode,
                "billingPhoneNumber": phone,
                "useForShipping": use_for_shipping,
            }
        }
        return self.execute(mutation, payload)

    def list_shipping_rates(self):
        query = """
        query CheckoutShippingRates {
          collectionShippingRates {
            id
            code
            label
            description
            method
            methodTitle
            price
            formattedPrice
            carrier
            carrierTitle
          }
        }
        """
        return self.execute(query)

    def save_shipping_method(self, shipping_method: str):
        mutation = """
        mutation createCheckoutShippingMethod($input: createCheckoutShippingMethodInput!) {
          createCheckoutShippingMethod(input: $input) {
            checkoutShippingMethod {
              success
              id
              message
            }
          }
        }
        """
        return self.execute(
            mutation,
            {"input": {"shippingMethod": shipping_method}},
        )

    def list_payment_methods(self):
        query = """
        query CheckoutPaymentMethods {
          collectionPaymentMethods {
            id
            method
            title
            description
            icon
            isAllowed
          }
        }
        """
        return self.execute(query)

    def save_payment_method(self, payment_method: str):
        mutation = """
        mutation createCheckoutPaymentMethod($input: createCheckoutPaymentMethodInput!) {
          createCheckoutPaymentMethod(input: $input) {
            checkoutPaymentMethod {
              success
              message
              paymentGatewayUrl
              paymentData
            }
          }
        }
        """
        return self.execute(
            mutation,
            {"input": {"paymentMethod": payment_method}},
        )

    def place_order(self):
        mutation = """
        mutation createCheckoutOrder {
          createCheckoutOrder(input: {}) {
            checkoutOrder {
              id
              orderId
              orderIncrementId
              success
              message
            }
          }
        }
        """
        return self.execute(mutation)
