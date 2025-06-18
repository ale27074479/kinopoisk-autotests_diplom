from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage


class AdvancedSearchPage(BasePage):
    """Страница расширенного поиска."""
    
    YEAR_FROM = (By.NAME, 'year_gte')
    YEAR_TO = (By.NAME, 'year_lte')
    GENRE_SELECT = (By.NAME, 'genre')
    SEARCH_BUTTON = (By.XPATH, "//button[contains(., 'Найти')]")
    RESULTS = (By.CSS_SELECTOR, ".search_results .movie")

    def set_year_range(self, from_year, to_year):
        """Установка диапазона годов."""
        self.fill_field(self.YEAR_FROM, str(from_year))
        self.fill_field(self.YEAR_TO, str(to_year))
        self.wait.until(EC.text_to_be_present_in_element_value(
            self.YEAR_FROM, str(from_year)))

    def select_genre(self, genre):
        """Выбор жанра."""
        self.click_element(self.GENRE_SELECT)
        genre_locator = (By.XPATH, f"//option[contains(., '{genre}')]")
        self.wait.until(EC.element_to_be_clickable(genre_locator))
        self.click_element(genre_locator)

    def submit_search(self):
        """Отправка формы поиска."""
        self.click_element(self.SEARCH_BUTTON)
        self.wait.until(EC.presence_of_element_located(self.RESULTS))

    def get_results(self):
        """Получение результатов поиска."""
        return self.find_elements(self.RESULTS)
    