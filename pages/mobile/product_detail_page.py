from __future__ import annotations

from pages.mobile.base_page import MobileBasePage


class ProductDetailPage(MobileBasePage):
    ADD_TO_CART = "Add to Cart"
    SUCCESS_MESSAGE = "Product added to cart successfully"

    def title(self, product_name: str):
        return self.wait_for_accessibility_id(product_name)

    def add_to_cart(self) -> None:
        self.tap_accessibility_id(self.ADD_TO_CART)

    def success_message(self):
        return self.wait_for_accessibility_id(self.SUCCESS_MESSAGE)
