import pytest

from pages.web.product_detail_page import ProductDetailPage
from pages.web.product_list_page import ProductListPage

@pytest.mark.contract
def test_product_name_consistency(playwright_page, web_base_url, storefront_product):
    product_list = ProductListPage(playwright_page, web_base_url)
    product_detail = ProductDetailPage(playwright_page, web_base_url)

    product_list.open_product_by_url_key(storefront_product["urlKey"])

    assert product_detail.get_name() == storefront_product["name"]
