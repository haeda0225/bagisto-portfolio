from __future__ import annotations

from pages.mobile.base_page import MobileBasePage


class CategoryPage(MobileBasePage):
    PRODUCTS_LABEL = "Products"
    CATEGORY_CHOICES = ("Electronics", "Furniture", "Fashion")

    def selected_category(self) -> str:
        return self.wait_for_any_accessibility_id(self.CATEGORY_CHOICES)

    def has_products_section(self) -> bool:
        return self.is_accessibility_id_visible(self.PRODUCTS_LABEL)

    def product_cards(self):
        return self.find_elements_by_xpath(
            "//android.widget.ImageView[contains(@content-desc, '$')]"
        )
