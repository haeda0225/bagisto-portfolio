import pytest

from pages.mobile.account_page import AccountPage
from pages.mobile.home_page import HomePage
from pages.mobile.login_page import LoginPage
from pages.mobile.navigation_page import NavigationPage


@pytest.mark.mobile
def test_mobile_login_screen_opens(mobile_driver):
    navigation = NavigationPage(mobile_driver)
    home = HomePage(mobile_driver)
    account = AccountPage(mobile_driver)
    login = LoginPage(mobile_driver)

    navigation.ensure_home()
    assert home.is_loaded()
    navigation.open_account()
    assert account.is_guest_account_screen()

    account.open_login()

    assert login.is_loaded()
    assert login.email_field().is_displayed()
    assert login.password_field().is_displayed()
    assert login.submit_button().is_displayed()
