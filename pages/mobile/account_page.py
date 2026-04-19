from __future__ import annotations

from pages.mobile.base_page import MobileBasePage


class AccountPage(MobileBasePage):
    WELCOME_TEXT = "Nice to see you here"
    LOGIN_BUTTON = "Login"
    SIGN_UP_BUTTON = "Sign Up"

    def is_guest_account_screen(self) -> bool:
        return self.is_accessibility_id_visible(self.WELCOME_TEXT)

    def open_login(self) -> None:
        self.tap_accessibility_id(self.LOGIN_BUTTON)
