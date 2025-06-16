from selenium.webdriver.common.by import By
from .base_page import BasePage
import time

class MoviesPage(BasePage):
    MOVIE_CARD = (By.CSS_SELECTOR, ".styles_root")
    GENRE_FILTER_BUTTON = (By.XPATH, "//button[contains(., 'Жанры')]")
    YEAR_FILTER_BUTTON = (By.XPATH, "//button[contains(., 'Годы')]")
    GENRE_ITEM = (By.XPATH, "//div[contains(@class, 'styles_dropdown')]//span[contains(., '{}')]")
    YEAR_ITEM = (By.XPATH, "//div[contains(@class, 'styles_dropdown')]//span[contains(., '{}')]")

    def open_genre_filter(self):
        self.click_element(self.GENRE_FILTER_BUTTON)
        time.sleep(1)

    def open_year_filter(self):
        self.click_element(self.YEAR_FILTER_BUTTON)
        time.sleep(1)

    def select_genre(self, genre_name):
        locator = (self.GENRE_ITEM[0], self.GENRE_ITEM[1].format(genre_name))
        self.click_element(locator)
        time.sleep(1)

    def select_year(self, year):
        locator = (self.YEAR_ITEM[0], self.YEAR_ITEM[1].format(year))
        self.click_element(locator)
        time.sleep(1)

    def get_movie_titles(self):
        movies = self.find_elements(self.MOVIE_CARD)
        return [movie.text for movie in movies if movie.text]
