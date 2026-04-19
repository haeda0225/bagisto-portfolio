from pages.base_page import BasePage


class CartPage(BasePage):
    def open_cart(self) -> None:
        self.open("/checkout/cart")

    def is_empty(self) -> bool:
        return "You don’t have a product in your cart." in self.page.locator("main").inner_text()

    def has_sign_in_entry(self) -> bool:
        return self.page.get_by_text("Sign In").count() > 0
