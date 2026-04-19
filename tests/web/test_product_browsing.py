import pytest

from pages.web.product_detail_page import ProductDetailPage
from pages.web.product_list_page import ProductListPage


@pytest.mark.web
def test_product_detail_smoke(playwright_page, web_base_url, storefront_product):
    product_list = ProductListPage(playwright_page, web_base_url)
    product_detail = ProductDetailPage(playwright_page, web_base_url)
    product_list.open_products()
    product_list.open_product_by_url_key(storefront_product["urlKey"])
    assert storefront_product["name"] in product_detail.get_name()
