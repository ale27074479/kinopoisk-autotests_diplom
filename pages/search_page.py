from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage


class SearchPage(BasePage):
    SEARCH_RESULTS = (By.CSS_SELECTOR, ".search_results .name")
    NO_RESULTS_MSG = (By.XPATH, "//*[contains(text(), 'ничего не найдено')]")

    def get_search_results_count(self):
        """Получение количества результатов поиска."""
        try:
            results = self.find_elements(self.SEARCH_RESULTS, timeout=5)
            return len(results)
        except:
            return 0

    def is_no_results(self):
        """Проверка отсутствия результатов."""
        return self.is_element_present(self.NO_RESULTS_MSG) or self.get_search_results_count() == 0

    def find_elements(self, locator, timeout=15):
        return self.wait.until(
            EC.presence_of_all_elements_located(locator),
            message=f"Не найдены элементы по локатору: {locator}")
