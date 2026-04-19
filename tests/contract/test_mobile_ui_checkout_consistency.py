import pytest

from api.clients.account_client import AccountClient
from api.clients.auth_client import AuthClient
from api.clients.product_client import ProductClient


@pytest.mark.contract
def test_mobile_ui_checkout_places_order_visible_in_api(
    mobile_adb,
    api_created_mobile_customer,
    checkout_address,
):
    address_response = AccountClient(
        token=api_created_mobile_customer["token"]
    ).add_customer_address(
        first_name=api_created_mobile_customer["first_name"],
        last_name=api_created_mobile_customer["last_name"],
        email=api_created_mobile_customer["email"],
        phone=api_created_mobile_customer["phone"],
        address1=checkout_address["address"],
        city=checkout_address["city"],
        state=checkout_address["state"],
        country=checkout_address["country"],
        postcode=checkout_address["postcode"],
    )
    assert address_response.status_code == 200, address_response.text

    address_payload = address_response.json()
    assert "errors" not in address_payload, address_payload
    assert address_payload["data"]["createAddUpdateCustomerAddress"][
        "addUpdateCustomerAddress"
    ]["id"]

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
    mobile_adb.tap_desc("Home", contains=True)
    mobile_adb.ensure_home_loaded()

    visible_names = []
    for desc in mobile_adb.all_content_descs():
        if "\n$" not in desc:
            continue
        name = desc.split("\n", 1)[0].strip()
        if name and name not in visible_names:
            visible_names.append(name)

    product_client = ProductClient()
    chosen_name = None
    for name in visible_names:
        response = product_client.search_products(query_text=name, first=5)
        assert response.status_code == 200, response.text
        payload = response.json()
        assert "errors" not in payload, payload
        for edge in payload["data"]["products"]["edges"]:
            node = edge["node"]
            if node["name"] == name and node.get("type") == "simple":
                chosen_name = name
                break
        if chosen_name:
            break

    assert chosen_name, "No visible simple product was found for mobile checkout."

    mobile_adb.tap_desc(chosen_name, contains=True)
    mobile_adb.wait_for_desc(chosen_name)
    mobile_adb.tap_desc("Add to Cart")
    mobile_adb.wait_for_desc("Product added to cart successfully")
    mobile_adb.back()
    mobile_adb.tap_desc("Cart", contains=True)
    mobile_adb.tap_desc("Pay Now")
    mobile_adb.wait_for_desc("Checkout", timeout=20)
    mobile_adb.swipe(540, 1800, 540, 900)
    mobile_adb.wait_for_desc("Free Shipping", contains=True, timeout=20)
    mobile_adb.tap_desc("Free Shipping", contains=True)
    mobile_adb.tap_desc("Money Transfer", contains=True)
    mobile_adb.tap_desc("Place Order")
    mobile_adb.wait_for_desc("Thank you for your order!", timeout=30)

    order_line = next(
        desc
        for desc in mobile_adb.all_content_descs()
        if desc.startswith("Your order No. #")
    )
    order_increment_id = order_line.split("#", 1)[1].strip()

    orders_response = AuthClient(token=api_created_mobile_customer["token"]).orders()
    assert orders_response.status_code == 200, orders_response.text

    orders_payload = orders_response.json()
    assert "errors" not in orders_payload, orders_payload
    orders = orders_payload["data"]["customerOrders"]["edges"]
    assert any(
        edge["node"]["incrementId"] == order_increment_id
        for edge in orders
    )
