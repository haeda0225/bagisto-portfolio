from api.clients.base_client import BaseClient


class ProductClient(BaseClient):
    def list_categories(self):
        query = """
        query Categories {
          categories {
            totalCount
            edges {
              node {
                id
                _id
                position
                logoUrl
                translation {
                  name
                  slug
                }
              }
            }
          }
        }
        """
        return self.execute(query)

    def list_products(self, first: int = 5):
        query = """
        query GetProducts($first: Int) {
          products(first: $first) {
            totalCount
            edges {
              node {
                id
                _id
                name
                urlKey
                price
                isSaleable
              }
            }
          }
        }
        """
        return self.execute(query, {"first": first})

    def search_products(self, query_text: str, first: int = 10):
        query = """
        query SearchProducts($query: String, $first: Int) {
          products(query: $query, first: $first) {
            totalCount
            edges {
              node {
                id
                _id
                name
                urlKey
                price
                isSaleable
                type
              }
            }
          }
        }
        """
        return self.execute(query, {"query": query_text, "first": first})
