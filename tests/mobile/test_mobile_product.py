import pytest

from pages.mobile.category_page import CategoryPage
from pages.mobile.home_page import HomePage
from pages.mobile.navigation_page import NavigationPage


@pytest.mark.mobile
def test_mobile_category_products_render(mobile_driver):
    navigation = NavigationPage(mobile_driver)
    home = HomePage(mobile_driver)
    category = CategoryPage(mobile_driver)

    navigation.ensure_home()
    assert home.is_loaded()
    assert home.has_featured_products_section()
    assert len(home.featured_product_cards()) >= 1

    navigation.open_categories()

    assert category.selected_category() in category.CATEGORY_CHOICES
    assert category.has_products_section()
    assert len(category.product_cards()) >= 1
