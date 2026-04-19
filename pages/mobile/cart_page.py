from __future__ import annotations

from pages.mobile.base_page import MobileBasePage


class CartPage(MobileBasePage):
    TITLE = "Cart"
    CONTINUE_SHOPPING = "Continue Shopping"
    EMPTY_CART = "Empty Cart"

    def is_loaded(self) -> bool:
        return self.is_accessibility_id_visible(self.TITLE)

    def item_title(self, product_name: str):
        return self.wait_for_accessibility_id(product_name)

    def item_summary(self, product_name: str):
        return self.wait_for_xpath(
            f"//*[contains(@content-desc, '{product_name}') or "
            f"contains(@content-desc, 'Units')]"
        )
