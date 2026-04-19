import pytest

@pytest.mark.contract
def test_mobile_product_name_consistency(mobile_adb, mobile_simple_product):
    mobile_adb.ensure_home_loaded()
    mobile_adb.tap_desc(mobile_simple_product["name"], contains=True)
    mobile_adb.wait_for_desc(mobile_simple_product["name"])
