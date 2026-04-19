import pytest

from pages.web.login_page import LoginPage


@pytest.mark.web
def test_customer_login_smoke(playwright_page, web_base_url, api_created_web_customer):
    login_page = LoginPage(playwright_page, web_base_url)
    login_page.open_login()
    login_page.login(
        api_created_web_customer["email"],
        api_created_web_customer["password"],
    )
    playwright_page.wait_for_load_state("networkidle")
    assert "/customer/login" in playwright_page.url
    assert "Verify your email account first." in playwright_page.locator("body").inner_text()
