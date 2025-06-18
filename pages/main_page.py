from selenium.webdriver.common.by import By

from pages.advanced_search_page import AdvancedSearchPage
from .base_page import BasePage
from .search_page import SearchPage

class MainPage(BasePage):
    SEARCH_FIELD = (By.XPATH, "//input[@placeholder='Фильмы, сериалы, персоны']")
    SEARCH_BUTTON = (By.XPATH, "//button[@type='submit']")
    ADVANCED_SEARCH_LINK = (By.XPATH, "//a[contains(@href, '/s/')]")

    def search_movie(self, movie_name):
        """Поиск фильма по названию."""
        self.fill_field(self.SEARCH_FIELD, movie_name)
        self.click_element(self.SEARCH_BUTTON)
        return SearchPage(self.driver)

    def go_to_advanced_search(self):
        """Переход на страницу расширенного поиска."""
        self.click_element(self.ADVANCED_SEARCH_LINK)
        return AdvancedSearchPage(self.driver)
