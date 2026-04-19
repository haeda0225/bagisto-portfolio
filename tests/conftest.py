import pytest
import subprocess
import time
from pathlib import Path
from uuid import uuid4

from api.clients.auth_client import AuthClient
from api.clients.product_client import ProductClient
from config.settings import (
    ADB_PATH,
    API_BASE_URL,
    APPIUM_SERVER_URL,
    MOBILE_CAPABILITIES,
    MOBILE_DEVICE_ID,
    STOREFRONT_KEY,
    WEB_BASE_URL,
    has_real_api_target,
)
from utils.mobile_adb_helper import MobileAdbHelper


@pytest.fixture(scope="session")
def web_base_url():
    return WEB_BASE_URL


@pytest.fixture(scope="session")
def api_base_url():
    return API_BASE_URL


@pytest.fixture(scope="session")
def mobile_capabilities():
    return MOBILE_CAPABILITIES


@pytest.fixture(autouse=True)
def ensure_api_target_configured(request):
    if "api" not in request.keywords:
        return

    if has_real_api_target():
        return

    pytest.skip(
        "API target is not configured. Set BAGISTO_API_BASE_URL and BAGISTO_STOREFRONT_KEY "
        f"(current api_base_url={API_BASE_URL!r}, storefront_key={STOREFRONT_KEY!r})."
    )


@pytest.fixture
def product_seed():
    return {"id": 1, "name": "Sample Product"}


@pytest.fixture
def registered_api_customer():
    uid = uuid4().hex[:12]
    phone_digits = "".join(str(int(char, 16) % 10) for char in uid[:8])

    return {
        "first_name": "QA",
        "last_name": "User",
        "email": f"qa_{uid}@example.com",
        "password": "Password123!",
        "phone": f"010{phone_digits}",
    }


@pytest.fixture
def api_created_web_customer(registered_api_customer):
    response = AuthClient().register_customer(
        first_name=registered_api_customer["first_name"],
        last_name=registered_api_customer["last_name"],
        email=registered_api_customer["email"],
        password=registered_api_customer["password"],
        phone=registered_api_customer["phone"],
    )
    assert response.status_code == 200, response.text

    payload = response.json()
    assert "errors" not in payload, payload
    return registered_api_customer


@pytest.fixture
def api_created_mobile_customer(registered_api_customer):
    response = AuthClient().register_customer(
        first_name=registered_api_customer["first_name"],
        last_name=registered_api_customer["last_name"],
        email=registered_api_customer["email"],
        password=registered_api_customer["password"],
        phone=registered_api_customer["phone"],
    )
    assert response.status_code == 200, response.text

    payload = response.json()
    assert "errors" not in payload, payload

    customer = dict(registered_api_customer)
    customer["token"] = payload["data"]["createCustomer"]["customer"]["token"]
    customer["api_token"] = payload["data"]["createCustomer"]["customer"]["apiToken"]
    return customer


@pytest.fixture
def checkout_address():
    return {
        "address": "123 Test Street",
        "city": "New York",
        "country": "US",
        "state": "New York",
        "postcode": "10001",
    }


@pytest.fixture
def storefront_product():
    response = ProductClient().list_products(first=1)
    assert response.status_code == 200, response.text

    payload = response.json()
    assert "errors" not in payload, payload
    return payload["data"]["products"]["edges"][0]["node"]


@pytest.fixture
def mobile_simple_product(mobile_adb):
    mobile_adb.force_stop("com.webkul.bagisto.mobikul")
    mobile_adb.start_app(
        package_name="com.webkul.bagisto.mobikul",
        activity_name="com.bagisto.bagisto_flutter.MainActivity",
    )
    mobile_adb.ensure_home_loaded()

    visible_names = []
    for desc in mobile_adb.all_content_descs():
        if "\n$" not in desc:
            continue
        name = desc.split("\n", 1)[0].strip()
        if name and name not in visible_names:
            visible_names.append(name)

    client = ProductClient()
    for name in visible_names:
        response = client.search_products(query_text=name, first=5)
        assert response.status_code == 200, response.text
        payload = response.json()
        assert "errors" not in payload, payload
        for edge in payload["data"]["products"]["edges"]:
            node = edge["node"]
            if node["name"] == name and node.get("type") == "simple":
                return node

    pytest.fail("No visible simple featured product was found for mobile tests.")


@pytest.fixture
def playwright_page():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        pytest.skip("Playwright is not installed.")

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            yield page
        finally:
            browser.close()


@pytest.fixture(scope="session")
def appium_server_url():
    return APPIUM_SERVER_URL


@pytest.fixture(scope="session")
def adb_path():
    return ADB_PATH


@pytest.fixture(scope="session")
def mobile_device_id():
    return MOBILE_DEVICE_ID


@pytest.fixture
def mobile_adb(adb_path, mobile_device_id):
    return MobileAdbHelper(adb_path=adb_path, device_id=mobile_device_id)


@pytest.fixture
def mobile_driver(mobile_capabilities, appium_server_url, adb_path, mobile_device_id):
    try:
        from appium import webdriver
        from appium.options.android import UiAutomator2Options
    except ImportError:
        pytest.skip("Appium client is not installed.")

    capabilities = dict(mobile_capabilities)
    capabilities.update(
        {
            "noReset": True,
            "newCommandTimeout": 120,
        }
    )

    adb = Path(adb_path)
    subprocess.run(
        [
            str(adb),
            "-s",
            mobile_device_id,
            "shell",
            "pm",
            "clear",
            capabilities["appPackage"],
        ],
        check=False,
    )
    subprocess.run(
        [
            str(adb),
            "-s",
            mobile_device_id,
            "shell",
            "am",
            "force-stop",
            capabilities["appPackage"],
        ],
        check=False,
    )
    subprocess.run(
        [
            str(adb),
            "-s",
            mobile_device_id,
            "shell",
            "am",
            "start",
            "-n",
            f"{capabilities['appPackage']}/{capabilities['appActivity']}",
        ],
        check=False,
    )

    options = UiAutomator2Options().load_capabilities(capabilities)

    driver = None
    last_exc = None
    for _ in range(2):
        try:
            driver = webdriver.Remote(appium_server_url, options=options)
            time.sleep(2)
            _ = driver.page_source
            break
        except Exception as exc:
            last_exc = exc
            if driver is not None:
                try:
                    driver.quit()
                except Exception:
                    pass
            driver = None
            time.sleep(2)

    if driver is None:
        pytest.skip(f"Appium session could not be stabilized: {last_exc}")

    driver.implicitly_wait(2)
    try:
        yield driver
    finally:
        driver.quit()
