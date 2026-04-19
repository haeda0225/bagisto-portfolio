from __future__ import annotations

from selenium.common.exceptions import TimeoutException

from pages.mobile.base_page import MobileBasePage


class NavigationPage(MobileBasePage):
    HOME_TAB = "Home"
    CATEGORIES_TAB = "Categories"
    CART_TAB = "Cart"
    ACCOUNT_TAB = "Account"

    def _tab_xpath(self, label: str) -> str:
        return f"//*[contains(@content-desc, '{label}')]"

    def open_home(self) -> None:
        self.tap_xpath(self._tab_xpath(self.HOME_TAB), timeout=10)

    def open_categories(self) -> None:
        self.tap_xpath(self._tab_xpath(self.CATEGORIES_TAB), timeout=10)

    def open_cart(self) -> None:
        self.tap_xpath(self._tab_xpath(self.CART_TAB), timeout=15)

    def open_account(self) -> None:
        self.tap_xpath(self._tab_xpath(self.ACCOUNT_TAB), timeout=10)

    def ensure_home(self) -> None:
        try:
            self.tap_xpath(self._tab_xpath(self.HOME_TAB), timeout=5)
        except TimeoutException:
            # Some intermediate screens can hide the bottom navigation briefly.
            self.driver.back()
            self.tap_xpath(self._tab_xpath(self.HOME_TAB), timeout=10)
