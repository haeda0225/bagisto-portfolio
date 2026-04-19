"""Common checkout helper functions to reduce code duplication."""

from __future__ import annotations

from api.clients.cart_client import CartClient
from api.clients.checkout_client import CheckoutClient


def complete_checkout_flow(
    token: str,
    customer: dict,
    checkout_address: dict,
    shipping_method: str = "free_free",
    payment_method: str = "moneytransfer",
) -> dict:
    """
    Complete the full checkout flow including address, shipping, payment, and order placement.

    Args:
        token: Customer authentication token
        customer: Customer data with first_name, last_name, email, phone
        checkout_address: Address data with address, city, country, state, postcode
        shipping_method: Shipping method code (default: "free_free")
        payment_method: Payment method code (default: "moneytransfer")

    Returns:
        dict: Created order data with 'id' and 'orderId'

    Raises:
        AssertionError: If any step fails
    """
    checkout_client = CheckoutClient(token=token)

    # Step 1: Save checkout address
    address_response = checkout_client.save_checkout_address(
        first_name=customer["first_name"],
        last_name=customer["last_name"],
        email=customer["email"],
        phone=customer["phone"],
        address=checkout_address["address"],
        city=checkout_address["city"],
        country=checkout_address["country"],
        state=checkout_address["state"],
        postcode=checkout_address["postcode"],
    )
    assert address_response.status_code == 200, address_response.text

    address_payload = address_response.json()
    assert "errors" not in address_payload, address_payload
    assert (
        address_payload["data"]["createCheckoutAddress"]["checkoutAddress"]["success"]
        is True
    ), "Failed to save checkout address"

    # Step 2: Save shipping method
    save_shipping_response = checkout_client.save_shipping_method(shipping_method)
    assert save_shipping_response.status_code == 200, save_shipping_response.text

    save_shipping_payload = save_shipping_response.json()
    assert "errors" not in save_shipping_payload, save_shipping_payload
    assert (
        save_shipping_payload["data"]["createCheckoutShippingMethod"][
            "checkoutShippingMethod"
        ]["success"]
        is True
    ), f"Failed to save shipping method: {shipping_method}"

    # Step 3: Save payment method
    save_payment_response = checkout_client.save_payment_method(payment_method)
    assert save_payment_response.status_code == 200, save_payment_response.text

    save_payment_payload = save_payment_response.json()
    assert "errors" not in save_payment_payload, save_payment_payload
    assert (
        save_payment_payload["data"]["createCheckoutPaymentMethod"][
            "checkoutPaymentMethod"
        ]["success"]
        is True
    ), f"Failed to save payment method: {payment_method}"

    # Step 4: Place order
    order_response = checkout_client.place_order()
    assert order_response.status_code == 200, order_response.text

    order_payload = order_response.json()
    assert "errors" not in order_payload, order_payload

    order = order_payload["data"]["createCheckoutOrder"]["checkoutOrder"]
    assert order["id"], "Order ID is missing"
    assert order["orderId"], "Order increment ID is missing"

    return order


def add_product_to_cart(token: str, product_id: str, quantity: int = 1) -> dict:
    """
    Add a product to the cart.

    Args:
        token: Customer authentication token
        product_id: Product ID to add
        quantity: Quantity to add (default: 1)

    Returns:
        dict: Cart response data

    Raises:
        AssertionError: If the operation fails
    """
    cart_response = CartClient(token=token).add_item(
        product_id=product_id,
        quantity=quantity,
    )
    assert cart_response.status_code == 200, cart_response.text

    cart_payload = cart_response.json()
    assert "errors" not in cart_payload, cart_payload
    assert (
        cart_payload["data"]["createAddProductInCart"]["addProductInCart"]["success"]
        is True
    ), "Failed to add product to cart"

    return cart_payload
