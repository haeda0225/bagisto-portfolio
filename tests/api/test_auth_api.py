import pytest

pytest.importorskip("requests")

from api.clients.auth_client import AuthClient
from api.schemas.auth_schema import LOGIN_REQUIRED_KEYS, REGISTER_REQUIRED_KEYS


@pytest.mark.api
def test_customer_registration_api(registered_api_customer):
    response = AuthClient().register_customer(
        first_name=registered_api_customer["first_name"],
        last_name=registered_api_customer["last_name"],
        email=registered_api_customer["email"],
        password=registered_api_customer["password"],
        phone=registered_api_customer["phone"],
    )

    assert response.status_code == 200
    payload = response.json()
    assert "errors" not in payload

    customer = payload["data"]["createCustomer"]["customer"]
    assert REGISTER_REQUIRED_KEYS.issubset(customer.keys())
    assert customer["email"] == registered_api_customer["email"]
    assert customer["token"]
    assert customer["apiToken"]


@pytest.mark.api
def test_customer_login_with_invalid_credentials_returns_failure():
    response = AuthClient().login_customer(
        email="john@example.com",
        password="demo123",
    )

    assert response.status_code == 200
    payload = response.json()
    assert "errors" not in payload

    login_result = payload["data"]["createCustomerLogin"]["customerLogin"]
    assert LOGIN_REQUIRED_KEYS.issubset(login_result.keys())
    assert login_result["success"] is False
    assert login_result["token"] == ""
    assert login_result["message"]


@pytest.mark.api
def test_api_created_customer_can_login_via_api(api_created_web_customer):
    response = AuthClient().login_customer(
        email=api_created_web_customer["email"],
        password=api_created_web_customer["password"],
    )

    assert response.status_code == 200
    payload = response.json()
    assert "errors" not in payload

    login_result = payload["data"]["createCustomerLogin"]["customerLogin"]
    assert login_result["success"] is True
    assert login_result["token"]
