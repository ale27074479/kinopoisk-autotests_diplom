from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage


class MoviesPage(BasePage):
    MOVIE_CARD = (By.CSS_SELECTOR, ".styles_root")
    GENRE_FILTER_BUTTON = (By.XPATH, "//button[contains(., 'Жанры')]")
    YEAR_FILTER_BUTTON = (By.XPATH, "//button[contains(., 'Годы')]")
    GENRE_ITEM = (By.XPATH, "//div[contains(@class, 'styles_dropdown')]//span[contains(., '{}')]")
    YEAR_ITEM = (By.XPATH, "//div[contains(@class, 'styles_dropdown')]//span[contains(., '{}')]")
    DROPDOWN_VISIBLE = (By.CSS_SELECTOR, "div[class*='styles_dropdown'][style*='display: block']")

    def open_genre_filter(self):
        self.click_element(self.GENRE_FILTER_BUTTON)
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.DROPDOWN_VISIBLE)
        )

    def open_year_filter(self):
        self.click_element(self.YEAR_FILTER_BUTTON)
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.DROPDOWN_VISIBLE)
        )

    def select_genre(self, genre_name):
        locator = (self.GENRE_ITEM[0], self.GENRE_ITEM[1].format(genre_name))
        self.click_element(locator)
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located(self.DROPDOWN_VISIBLE)
        )

    def select_year(self, year):
        locator = (self.YEAR_ITEM[0], self.YEAR_ITEM[1].format(year))
        self.click_element(locator)
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located(self.DROPDOWN_VISIBLE)
        )

    def get_movie_titles(self):
        movies = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(self.MOVIE_CARD)
        )
        return [movie.text for movie in movies if movie.text]
    