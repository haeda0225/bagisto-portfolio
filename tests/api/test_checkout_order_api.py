import pytest

from api.clients.auth_client import AuthClient
from api.clients.product_client import ProductClient
from utils.checkout_helper import add_product_to_cart, complete_checkout_flow


@pytest.mark.api
def test_logged_in_customer_can_place_order(api_created_mobile_customer, checkout_address):
    # Find a product to order
    product_response = ProductClient().search_products(
        query_text="Arctic Touchscreen Winter Gloves",
        first=5,
    )
    assert product_response.status_code == 200, product_response.text

    product_payload = product_response.json()
    assert "errors" not in product_payload, product_payload
    product = product_payload["data"]["products"]["edges"][0]["node"]

    # Add product to cart
    add_product_to_cart(
        token=api_created_mobile_customer["token"],
        product_id=product["_id"],
        quantity=1,
    )

    # Complete checkout flow
    order = complete_checkout_flow(
        token=api_created_mobile_customer["token"],
        customer=api_created_mobile_customer,
        checkout_address=checkout_address,
    )

    # Verify order appears in customer orders
    orders_response = AuthClient(token=api_created_mobile_customer["token"]).orders()
    assert orders_response.status_code == 200, orders_response.text

    orders_payload = orders_response.json()
    assert "errors" not in orders_payload, orders_payload
    orders = orders_payload["data"]["customerOrders"]
    assert orders["totalCount"] == 1
    assert orders["edges"][0]["node"]["incrementId"] == str(order["orderId"])
