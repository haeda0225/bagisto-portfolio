from __future__ import annotations

from typing import Iterable

from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class MobileBasePage:
    def __init__(self, driver, timeout: int = 20) -> None:
        self.driver = driver
        self.timeout = timeout

    def wait_for_accessibility_id(self, value: str, timeout: int | None = None):
        return WebDriverWait(self.driver, timeout or self.timeout).until(
            EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, value))
        )

    def wait_for_id(self, value: str, timeout: int | None = None):
        locator = (
            AppiumBy.XPATH,
            f"//*[@resource-id='{value}' or "
            f"@resource-id='com.webkul.bagisto.mobikul:id/{value}']",
        )
        return WebDriverWait(self.driver, timeout or self.timeout).until(
            EC.presence_of_element_located(locator)
        )

    def tap_accessibility_id(self, value: str, timeout: int | None = None) -> None:
        WebDriverWait(self.driver, timeout or self.timeout).until(
            EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, value))
        ).click()

    def tap_id(self, value: str, timeout: int | None = None) -> None:
        locator = (
            AppiumBy.XPATH,
            f"//*[@resource-id='{value}' or "
            f"@resource-id='com.webkul.bagisto.mobikul:id/{value}']",
        )
        WebDriverWait(self.driver, timeout or self.timeout).until(
            EC.element_to_be_clickable(locator)
        ).click()

    def is_accessibility_id_visible(self, value: str, timeout: int = 5) -> bool:
        try:
            self.wait_for_accessibility_id(value, timeout=timeout)
            return True
        except TimeoutException:
            return False

    def find_elements_by_xpath(self, value: str):
        return self.driver.find_elements(AppiumBy.XPATH, value)

    def wait_for_xpath(self, value: str, timeout: int | None = None):
        return WebDriverWait(self.driver, timeout or self.timeout).until(
            EC.presence_of_element_located((AppiumBy.XPATH, value))
        )

    def tap_xpath(self, value: str, timeout: int | None = None) -> None:
        WebDriverWait(self.driver, timeout or self.timeout).until(
            EC.element_to_be_clickable((AppiumBy.XPATH, value))
        ).click()

    def wait_for_any_accessibility_id(
        self,
        values: Iterable[str],
        timeout: int | None = None,
    ) -> str:
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        for value in values:
            try:
                wait.until(
                    EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, value))
                )
                return value
            except TimeoutException:
                continue
        raise TimeoutException(f"None of the accessibility ids became visible: {values}")
