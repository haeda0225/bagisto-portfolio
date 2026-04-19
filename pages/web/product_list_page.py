from pages.base_page import BasePage


class ProductListPage(BasePage):
    def open_products(self) -> None:
        self.open("/")

    def open_product_by_url_key(self, url_key: str) -> None:
        self.open(f"/{url_key}")
