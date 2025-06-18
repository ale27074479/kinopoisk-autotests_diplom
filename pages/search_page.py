from selenium.webdriver.common.by import By
from .base_page import BasePage

class SearchPage(BasePage):
    SEARCH_RESULTS = (By.XPATH, "//div[@data-testid='search-results']//div[contains(@class, 'styles_root')]")
    NO_RESULTS = (By.XPATH, "//div[contains(text(), 'ничего не найдено')]")

    def get_search_results(self):
        """Получение результатов поиска."""
        return self.find_elements(self.SEARCH_RESULTS)

    def is_no_results(self):
        """Проверка отсутствия результатов."""
        try:
            return bool(self.find_element(self.NO_RESULTS))
        except Exception:
            return False
