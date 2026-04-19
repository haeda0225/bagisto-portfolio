from pages.base_page import BasePage


class ProductDetailPage(BasePage):
    PRODUCT_NAME = "h1"

    def get_name(self) -> str:
        return self.text(self.PRODUCT_NAME)

    def has_add_to_cart_button(self) -> bool:
        return self.page.get_by_role("button", name="Add To Cart").count() > 0
