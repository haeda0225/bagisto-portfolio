import pytest

from pages.web.cart_page import CartPage
from pages.web.product_detail_page import ProductDetailPage
from pages.web.product_list_page import ProductListPage


@pytest.mark.web
def test_add_to_cart_smoke(playwright_page, web_base_url, storefront_product):
    product_list = ProductListPage(playwright_page, web_base_url)
    product_detail = ProductDetailPage(playwright_page, web_base_url)
    cart_page = CartPage(playwright_page, web_base_url)

    product_list.open_products()
    product_list.open_product_by_url_key(storefront_product["urlKey"])
    assert storefront_product["name"] in product_detail.get_name()
    assert product_detail.has_add_to_cart_button()
    cart_page.open_cart()
    assert cart_page.is_empty() or cart_page.has_sign_in_entry()
