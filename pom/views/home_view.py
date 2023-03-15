from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class HomeView(object):
    ECHO_ITEM = (MobileBy.ACCESSIBILITY_ID, 'Echo Box')

    def nav_to_echo_box(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located(self.ECHO_ITEM)).click()

    def __init__(self, driver):
        self.driver = driver
