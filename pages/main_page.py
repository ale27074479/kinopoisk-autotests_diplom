from selenium.webdriver.common.by import By
from .base_page import BasePage


class MainPage(BasePage):
    SEARCH_FIELD = (By.XPATH, "//input[@placeholder='Фильмы, сериалы, персоны']")
    SEARCH_BUTTON = (By.XPATH, "//button[@type='submit']")

    def search_movie(self, movie_name):
        field = self.find_element(self.SEARCH_FIELD)
        field.clear()
        field.send_keys(movie_name)
        self.click_element(self.SEARCH_BUTTON)
        from pages.search_page import SearchPage
        return SearchPage(self.driver)
