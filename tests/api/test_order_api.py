import pytest

pytest.importorskip("requests")

from api.clients.auth_client import AuthClient


@pytest.mark.api
def test_get_customer_orders_api(registered_api_customer):
    register_response = AuthClient().register_customer(
        first_name=registered_api_customer["first_name"],
        last_name=registered_api_customer["last_name"],
        email=registered_api_customer["email"],
        password=registered_api_customer["password"],
        phone=registered_api_customer["phone"],
    )
    assert register_response.status_code == 200

    register_payload = register_response.json()
    assert "errors" not in register_payload
    token = register_payload["data"]["createCustomer"]["customer"]["token"]

    client = AuthClient(token=token)
    orders_response = client.orders()
    assert orders_response.status_code == 200

    orders_payload = orders_response.json()
    assert "errors" not in orders_payload

    orders = orders_payload["data"]["customerOrders"]
    assert orders["totalCount"] == 0
    assert orders["edges"] == []
