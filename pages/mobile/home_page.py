from __future__ import annotations

from pages.mobile.base_page import MobileBasePage


class HomePage(MobileBasePage):
    HEADER = "bagisto"
    FEATURED_PRODUCTS = "Featured Products"

    def is_loaded(self) -> bool:
        return self.is_accessibility_id_visible(self.HEADER)

    def has_featured_products_section(self) -> bool:
        return self.is_accessibility_id_visible(self.FEATURED_PRODUCTS)

    def featured_product_cards(self):
        return self.find_elements_by_xpath(
            "//android.widget.ImageView[contains(@content-desc, '$')]"
        )

    def open_featured_product(self, product_name: str) -> None:
        self.tap_xpath(
            f"//android.widget.ImageView[contains(@content-desc, \"{product_name}\")]"
        )
