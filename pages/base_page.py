import os
from dotenv import load_dotenv
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

load_dotenv()

class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.base_url = os.getenv('KINOPOISK_URL', 'https://www.kinopoisk.ru')
        self.wait = WebDriverWait(driver, 15)

    def open(self):
        self.driver.get(self.base_url)
        time.sleep(2)

    def find_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_elements(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click_element(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script("arguments[0].click();", element)

    def fill_field(self, locator, text):
        field = self.find_element(locator)
        field.clear()
        field.send_keys(text)

    def accept_cookies(self):
        try:
            cookie_banner = (By.CSS_SELECTOR, ".cookies button")
            self.click_element(cookie_banner)
            time.sleep(1)
        except:
            pass
