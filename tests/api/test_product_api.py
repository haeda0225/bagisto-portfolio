import pytest

pytest.importorskip("requests")

from api.clients.product_client import ProductClient
from api.schemas.product_schema import CATEGORY_REQUIRED_KEYS, PRODUCT_REQUIRED_KEYS


@pytest.mark.api
def test_category_list_api():
    response = ProductClient().list_categories()
    assert response.status_code == 200
    payload = response.json()
    assert "errors" not in payload

    categories = payload["data"]["categories"]
    assert categories["totalCount"] >= 1
    assert categories["edges"]
    assert CATEGORY_REQUIRED_KEYS.issubset(categories["edges"][0]["node"].keys())


@pytest.mark.api
def test_product_list_api():
    response = ProductClient().list_products(first=5)
    assert response.status_code == 200
    payload = response.json()
    assert "errors" not in payload

    products = payload["data"]["products"]
    assert products["totalCount"] >= 1
    assert products["edges"]
    assert PRODUCT_REQUIRED_KEYS.issubset(products["edges"][0]["node"].keys())
