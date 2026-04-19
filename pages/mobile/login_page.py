from __future__ import annotations

from pages.mobile.base_page import MobileBasePage


class LoginPage(MobileBasePage):
    EMAIL_FIELD_ID = "login_email_field"
    PASSWORD_FIELD_ID = "login_password_field"
    SUBMIT_BUTTON_ID = "login_submit_button"
    WELCOME_TEXT = "Welcome back!"

    def is_loaded(self) -> bool:
        return self.is_accessibility_id_visible(self.WELCOME_TEXT)

    def email_field(self):
        return self.wait_for_id(self.EMAIL_FIELD_ID)

    def password_field(self):
        return self.wait_for_id(self.PASSWORD_FIELD_ID)

    def submit_button(self):
        return self.wait_for_id(self.SUBMIT_BUTTON_ID)
