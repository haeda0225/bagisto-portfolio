from pages.base_page import BasePage


class CheckoutPage(BasePage):
    def open_checkout(self) -> None:
        self.open("/checkout/onepage")

    def is_checkout_page(self) -> bool:
        return "checkout" in self.page.url.lower()
