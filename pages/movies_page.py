from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from .base_page import BasePage
import time
import allure


class AdvancedSearchPage(BasePage):
    GENRE_BUTTON = (By.XPATH, "//button[.//div[contains(text(), 'Жанры')]]")
    GENRE_OPTION = (By.XPATH, "//div[@role='option' and contains(., '{}')]")
    YEAR_FROM = (By.XPATH, "//input[@placeholder='от']")
    YEAR_TO = (By.XPATH, "//input[@placeholder='до']")
    SEARCH_BUTTON = (By.XPATH, "//button[contains(., 'поиск')]")
    RESULTS = (By.CSS_SELECTOR, ".styles_root__ti07r .styles_mainTitle__iwd6f")
    LOADER = (By.CSS_SELECTOR, ".styles_loader__DqBXi")

    @allure.step("Выбираем жанр '{genre_name}'")
    def select_genre(self, genre_name):
        try:
            # Явное ожидание и прокрутка к элементу
            button = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(self.GENRE_BUTTON)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
            
            # Дополнительное ожидание кликабельности
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.GENRE_BUTTON)
            ).click()
            
            # Выбор жанра
            genre_locator = (self.GENRE_OPTION[0], self.GENRE_OPTION[1].format(genre_name))
            self.click_element(genre_locator)
            time.sleep(1)
        except Exception as e:
            self._take_screenshot("genre_selection_error")
            raise

    @allure.step("Устанавливаем диапазон годов {from_year}-{to_year}")
    def set_year_range(self, from_year, to_year):
        try:
            # Ожидание и заполнение полей года
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.YEAR_FROM)
            ).send_keys(str(from_year))
            
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.YEAR_TO)
            ).send_keys(str(to_year))
            time.sleep(1)
        except Exception as e:
            self._take_screenshot("year_range_error")
            raise

    @allure.step("Выполняем поиск")
    def perform_search(self):
        try:
            self.click_element(self.SEARCH_BUTTON)
            self.wait_for_loader_to_disappear()
            time.sleep(2)  # Дополнительное ожидание после поиска
        except Exception as e:
            self._take_screenshot("search_error")
            raise

    def wait_for_loader_to_disappear(self):
        WebDriverWait(self.driver, 30).until(
            EC.invisibility_of_element_located(self.LOADER),
            message="Лоадер не исчез за 30 секунд"
        )

    def get_results_titles(self):
        try:
            elements = WebDriverWait(self.driver, 20).until(
                EC.presence_of_all_elements_located(self.RESULTS)
            )
            return [el.text for el in elements if el.text]
        except Exception as e:
            self._take_screenshot("results_error")
            return []
   