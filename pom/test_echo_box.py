from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from views.home_view import HomeView
from views.home_view import EchoView

def test_echo_box(driver):
    home = HomeView(driver)
    home.nav_to_echo_box()

    message = 'Hello'
    echo = EchoView(driver)
    echo.save_message(message)
    assert echo.read_message() == message
    echo.nav_back()

    home.nav_to_echo_box()
    assert echo.read_message() == message
