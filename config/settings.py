from __future__ import annotations

import json
import os
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_ENV_FILE = ROOT_DIR / "config" / "environments" / "dev.json"


def load_env_config() -> dict:
    env_file = Path(os.getenv("BAGISTO_ENV_FILE", DEFAULT_ENV_FILE))
    with env_file.open(encoding="utf-8") as fp:
        return json.load(fp)


SETTINGS = load_env_config()


WEB_BASE_URL = os.getenv(
    "BAGISTO_WEB_BASE_URL",
    SETTINGS.get("web_base_url", SETTINGS.get("base_url", "")),
)
API_BASE_URL = os.getenv(
    "BAGISTO_API_BASE_URL",
    SETTINGS.get("api_base_url", SETTINGS.get("base_url", "")),
)
STOREFRONT_KEY = os.getenv("BAGISTO_STOREFRONT_KEY", SETTINGS["storefront_key"])
API_TIMEOUT = int(os.getenv("BAGISTO_API_TIMEOUT", SETTINGS.get("api_timeout", 15)))
HEADLESS = str(os.getenv("PW_HEADLESS", SETTINGS.get("headless", True))).lower() == "true"

MOBILE_CAPABILITIES = SETTINGS["mobile"]
APPIUM_SERVER_URL = os.getenv(
    "APPIUM_SERVER_URL",
    SETTINGS["mobile"].get("appium_server_url", "http://127.0.0.1:4723"),
)
ADB_PATH = os.getenv(
    "ADB_PATH",
    SETTINGS["mobile"].get("adb_path", "adb"),
)
MOBILE_DEVICE_ID = os.getenv(
    "MOBILE_DEVICE_ID",
    SETTINGS["mobile"].get("udid", "emulator-5554"),
)


def has_real_api_target() -> bool:
    normalized_base_url = API_BASE_URL.rstrip("/").lower()
    storefront_key = STOREFRONT_KEY.strip().lower()

    invalid_base_urls = {
        "",
        "http://localhost",
        "https://localhost",
        "http://127.0.0.1",
        "https://127.0.0.1",
    }
    invalid_storefront_keys = {
        "",
        "replace-with-real-storefront-key",
    }

    return normalized_base_url not in invalid_base_urls and storefront_key not in invalid_storefront_keys
