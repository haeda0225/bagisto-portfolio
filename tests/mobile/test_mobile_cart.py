import pytest


@pytest.mark.mobile
def test_mobile_cart_tab_renders(mobile_adb):
    mobile_adb.clear_app_data("com.webkul.bagisto.mobikul")
    mobile_adb.start_app(
        package_name="com.webkul.bagisto.mobikul",
        activity_name="com.bagisto.bagisto_flutter.MainActivity",
    )
    mobile_adb.ensure_home_loaded()
    mobile_adb.tap_desc("Cart", contains=True)
    mobile_adb.wait_for_desc("Cart")


@pytest.mark.mobile
def test_mobile_add_simple_product_to_cart(mobile_adb, mobile_simple_product):
    mobile_adb.ensure_home_loaded()
    mobile_adb.tap_desc(mobile_simple_product["name"], contains=True)
    mobile_adb.wait_for_desc(mobile_simple_product["name"])
    mobile_adb.tap_desc("Add to Cart")
    mobile_adb.wait_for_desc("Product added to cart successfully")
    mobile_adb.back()
    mobile_adb.tap_desc("Cart", contains=True)
    mobile_adb.wait_for_desc("Cart")
    mobile_adb.wait_for_desc(mobile_simple_product["name"])
