from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from .base_page import BasePage
import time
import re
import allure


class MoviePage(BasePage):
    # Универсальные локаторы для рейтинга
    RATING_VALUE = (By.XPATH, "//div[contains(@class, 'film-rating')]//span[contains(@class, 'rating-value')]")
    
    @allure.step("Проверить отображение рейтинга")
    def is_rating_displayed(self):
        try:
            WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located(self.RATING_VALUE)
            )
            return True
        except:
            self._take_screenshot("rating_not_displayed")
            return False

    @allure.step("Получить значение рейтинга")
    def get_movie_rating(self):
        try:
            rating_element = WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located(self.RATING_VALUE)
            )
            rating_text = rating_element.text.strip()
            # Извлекаем только числовое значение
            rating_value = re.search(r'[\d.]+', rating_text)
            if rating_value:
                return float(rating_value.group())
            return 0
        except Exception as e:
            self._take_screenshot("rating_error")
            return 0
