from selenium.webdriver.common.by import By
from .base_page import BasePage

class MainPage(BasePage):
    SEARCH_FIELD = (By.NAME, 'kp_query')
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    ADVANCED_SEARCH_LINK = (By.LINK_TEXT, "Расширенный поиск")
    LOGIN_BUTTON = (By.CSS_SELECTOR, ".header__login-button")

    def search_movie(self, movie_name):
        self.fill_field(self.SEARCH_FIELD, movie_name)
        self.click_element(self.SEARCH_BUTTON)

    def go_to_advanced_search(self):
        self.click_element(self.ADVANCED_SEARCH_LINK)

    def click_login_button(self):
        self.click_element(self.LOGIN_BUTTON)
