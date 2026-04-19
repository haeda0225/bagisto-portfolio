from pages.base_page import BasePage


class LoginPage(BasePage):
    def open_login(self) -> None:
        self.open("/customer/login")

    def login(self, email: str, password: str) -> None:
        self.page.locator("input[name='email']").fill(email)
        self.page.locator("input[name='password']").fill(password)
        self.page.get_by_role("button", name="Sign In").click()
