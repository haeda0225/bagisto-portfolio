import pytest

from api.clients.cart_client import CartClient
from api.clients.checkout_client import CheckoutClient
from api.clients.product_client import ProductClient


@pytest.mark.contract
def test_api_order_appears_in_mobile_order_history(
    mobile_adb,
    api_created_mobile_customer,
    checkout_address,
):
    product_response = ProductClient().search_products(
        query_text="Arctic Touchscreen Winter Gloves",
        first=5,
    )
    assert product_response.status_code == 200, product_response.text

    product_payload = product_response.json()
    assert "errors" not in product_payload, product_payload
    product = product_payload["data"]["products"]["edges"][0]["node"]

    cart_response = CartClient(token=api_created_mobile_customer["token"]).add_item(
        product_id=product["_id"],
        quantity=1,
    )
    assert cart_response.status_code == 200, cart_response.text

    cart_payload = cart_response.json()
    assert "errors" not in cart_payload, cart_payload
    assert (
        cart_payload["data"]["createAddProductInCart"]["addProductInCart"]["success"]
        is True
    )

    checkout_client = CheckoutClient(token=api_created_mobile_customer["token"])

    address_response = checkout_client.save_checkout_address(
        first_name=api_created_mobile_customer["first_name"],
        last_name=api_created_mobile_customer["last_name"],
        email=api_created_mobile_customer["email"],
        phone=api_created_mobile_customer["phone"],
        address=checkout_address["address"],
        city=checkout_address["city"],
        country=checkout_address["country"],
        state=checkout_address["state"],
        postcode=checkout_address["postcode"],
    )
    assert address_response.status_code == 200, address_response.text

    address_payload = address_response.json()
    assert "errors" not in address_payload, address_payload

    shipping_response = checkout_client.save_shipping_method("free_free")
    assert shipping_response.status_code == 200, shipping_response.text
    shipping_payload = shipping_response.json()
    assert "errors" not in shipping_payload, shipping_payload

    payment_response = checkout_client.save_payment_method("moneytransfer")
    assert payment_response.status_code == 200, payment_response.text
    payment_payload = payment_response.json()
    assert "errors" not in payment_payload, payment_payload

    order_response = checkout_client.place_order()
    assert order_response.status_code == 200, order_response.text

    order_payload = order_response.json()
    assert "errors" not in order_payload, order_payload
    order = order_payload["data"]["createCheckoutOrder"]["checkoutOrder"]
    order_increment_id = str(order["orderId"])

    mobile_adb.clear_app_data("com.webkul.bagisto.mobikul")
    mobile_adb.start_app(
        package_name="com.webkul.bagisto.mobikul",
        activity_name="com.bagisto.bagisto_flutter.MainActivity",
    )
    mobile_adb.ensure_home_loaded()
    mobile_adb.tap_desc("Account", contains=True)
    mobile_adb.tap_desc("Login")
    mobile_adb.fill_resource_id(
        "login_email_field",
        api_created_mobile_customer["email"],
    )
    mobile_adb.fill_resource_id(
        "login_password_field",
        api_created_mobile_customer["password"],
    )
    mobile_adb.tap_desc("Login")
    mobile_adb.wait_for_desc(api_created_mobile_customer["email"], contains=True, timeout=20)
    mobile_adb.tap_desc("My Orders", contains=True)
    mobile_adb.wait_for_desc(f"#{order_increment_id}", contains=True, timeout=20)
