import pytest

pytest.importorskip("requests")

from api.clients.cart_client import CartClient
from api.clients.product_client import ProductClient


@pytest.mark.api
def test_create_guest_cart_and_add_product_api():
    product_response = ProductClient().list_products(first=1)
    assert product_response.status_code == 200
    product_payload = product_response.json()
    assert "errors" not in product_payload

    first_product = product_payload["data"]["products"]["edges"][0]["node"]
    product_id = first_product["_id"]

    cart_response = CartClient().create_cart_token()
    assert cart_response.status_code == 200
    cart_payload = cart_response.json()
    assert "errors" not in cart_payload

    cart_token = cart_payload["data"]["createCartToken"]["cartToken"]
    assert cart_token["success"] is True
    assert cart_token["isGuest"] is True
    assert cart_token["sessionToken"]

    add_response = CartClient(token=cart_token["sessionToken"]).add_item(
        product_id=product_id,
        quantity=1,
    )
    assert add_response.status_code == 200
    add_payload = add_response.json()
    assert "errors" not in add_payload

    cart_data = add_payload["data"]["createAddProductInCart"]["addProductInCart"]
    assert cart_data["success"] is True
    assert cart_data["itemsCount"] >= 1
    assert any(
        item["node"]["productId"] == product_id
        for item in cart_data["items"]["edges"]
    )
