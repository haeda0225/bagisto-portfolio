import pytest

from pages.web.checkout_page import CheckoutPage


@pytest.mark.web
def test_checkout_entry_smoke(playwright_page, web_base_url):
    checkout_page = CheckoutPage(playwright_page, web_base_url)
    checkout_page.open_checkout()
    playwright_page.wait_for_load_state("networkidle")
    assert checkout_page.is_checkout_page()
