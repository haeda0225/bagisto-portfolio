import pytest

from api.clients.auth_client import AuthClient


@pytest.mark.contract
def test_mobile_login_and_empty_orders_consistency(mobile_adb, api_created_mobile_customer):
    api_client = AuthClient(token=api_created_mobile_customer["token"])
    orders_response = api_client.orders()
    assert orders_response.status_code == 200, orders_response.text

    orders_payload = orders_response.json()
    assert "errors" not in orders_payload, orders_payload
    assert orders_payload["data"]["customerOrders"]["totalCount"] == 0
    assert orders_payload["data"]["customerOrders"]["edges"] == []

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
    mobile_adb.wait_for_desc("No Orders Yet", timeout=20)
