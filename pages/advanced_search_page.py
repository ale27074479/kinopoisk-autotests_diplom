from selenium.webdriver.common.by import By
from .base_page import BasePage
import time

class AdvancedSearchPage(BasePage):
    YEAR_FROM = (By.NAME, 'year_gte')
    YEAR_TO = (By.NAME, 'year_lte')
    GENRE_SELECT = (By.NAME, 'genre')
    SEARCH_BUTTON = (By.XPATH, "//button[contains(., 'Найти')]")
    RESULTS = (By.CSS_SELECTOR, ".search_results .movie")

    def set_year_range(self, from_year, to_year):
        self.fill_field(self.YEAR_FROM, str(from_year))
        self.fill_field(self.YEAR_TO, str(to_year))
        time.sleep(1)

    def select_genre(self, genre):
        self.click_element(self.GENRE_SELECT)
        genre_locator = (By.XPATH, f"//option[contains(., '{genre}')]")
        self.click_element(genre_locator)
        time.sleep(1)

    def submit_search(self):
        self.click_element(self.SEARCH_BUTTON)
        time.sleep(2)

    def get_results(self):
        return self.find_elements(self.RESULTS)
