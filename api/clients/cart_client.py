from api.clients.base_client import BaseClient


class CartClient(BaseClient):
    def create_cart_token(self):
        mutation = """
        mutation CreateCart {
          createCartToken(input: {}) {
            cartToken {
              id
              cartToken
              sessionToken
              success
              message
              isGuest
            }
          }
        }
        """
        return self.execute(mutation)

    def add_item(self, product_id: int, quantity: int = 1):
        mutation = """
        mutation AddSimpleProductToCart($productId: Int!, $quantity: Int!) {
          createAddProductInCart(
            input: {
              productId: $productId
              quantity: $quantity
            }
          ) {
            addProductInCart {
              id
              itemsCount
              itemsQty
              success
              message
              isGuest
              items {
                edges {
                  node {
                    productId
                    quantity
                    name
                  }
                }
              }
            }
          }
        }
        """
        return self.execute(
            mutation,
            {"productId": product_id, "quantity": quantity},
        )
