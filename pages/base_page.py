from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from helpers.retry import retry
import time

class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.base_url = "https://www.kinopoisk.ru"
        self.wait = WebDriverWait(driver, 15)
    
    def open(self, path=''):
        self.driver.get(f"{self.base_url}{path}")
        self.wait_for_page_loaded()
    
    def wait_for_page_loaded(self):
        time.sleep(1)  # Базовое ожидание
        self.wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')
    
    @retry(max_attempts=3, delay=1)
    def find_element(self, locator):
        try:
            return self.wait.until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            print(f"Element not found: {locator}")
            raise
    
    @retry(max_attempts=3, delay=1)
    def click_element(self, locator):
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            element.click()
        except TimeoutException:
            print(f"Element not clickable: {locator}")
            raise
    
    @retry(max_attempts=3, delay=1)
    def fill_field(self, locator, text):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
    
    def accept_cookies(self):
        try:
            cookie_accept = (By.XPATH, "//button[contains(., 'Принимаю')]")
            self.click_element(cookie_accept)
        except Exception:
            pass
