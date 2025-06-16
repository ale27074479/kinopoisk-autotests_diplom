from selenium.webdriver.common.by import By
from .base_page import BasePage

class SearchPage(BasePage):
    SEARCH_RESULTS = (By.CSS_SELECTOR, ".search_results .styles_root")
    NO_RESULTS = (By.CSS_SELECTOR, ".no-results")

    def get_search_results(self):
        return self.find_elements(self.SEARCH_RESULTS)

    def is_no_results(self):
        return len(self.driver.find_elements(*self.NO_RESULTS)) > 0
