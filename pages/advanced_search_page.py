from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import allure


class AdvancedSearchPage:
    SEARCH_BUTTON_LOCATORS = [
        (By.CSS_SELECTOR, "input.el_18.submit[type='button']"),
        (By.XPATH, "//input[@value='поиск' and contains(@class, 'submit')]"),
        (By.XPATH, "//input[@onclick[contains(., 'document.film_search.submit')]]")
    ]
    KEYWORD_INPUT = (By.NAME, "m_act[find]")
    COOKIE_ACCEPT_BTN = (By.XPATH, "//button[contains(., 'Принимаю')]")
    RESULTS_LOCATOR = (By.CSS_SELECTOR, "div.search_results, div.results")
    FILM_TITLES = (By.CSS_SELECTOR, "div.info .name a")

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def _take_screenshot(self, name: str) -> None:
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name=name,
            attachment_type=allure.attachment_type.PNG
        )

    @allure.step("Принять куки если есть")
    def accept_cookies(self) -> None:
        try:
            self.wait.until(EC.element_to_be_clickable(self.COOKIE_ACCEPT_BTN)).click()
            time.sleep(1)
            self._take_screenshot("cookies_accepted")
        except Exception:
            pass

    @allure.step("Найти кнопку поиска")
    def _find_search_button(self):
        for locator in self.SEARCH_BUTTON_LOCATORS:
            try:
                element = self.wait.until(EC.element_to_be_clickable(locator))
                self._take_screenshot(f"found_button_{locator}")
                return element
            except Exception as e:
                print(f"Не удалось найти кнопку поиска по локатору {locator}: {str(e)}")
                continue
        raise Exception("Не удалось найти кнопку поиска после проверки всех локаторов")

    @allure.step("Ввести ключевое слово '{keyword}'")
    def search_by_keyword(self, keyword: str) -> None:
        try:
            input_field = self.wait.until(EC.element_to_be_clickable(self.KEYWORD_INPUT))
            input_field.clear()
            input_field.send_keys(keyword)
            self._take_screenshot("keyword_entered")
        except Exception as e:
            self._take_screenshot("keyword_input_error")
            raise Exception(f"Ошибка при вводе ключевого слова: {str(e)}")

    @allure.step("Выполнить поиск")
    def perform_search(self) -> None:
        try:
            search_btn = self._find_search_button()
            
            if search_btn.get_attribute("disabled"):
                self._fill_mandatory_fields()
                search_btn = self._find_search_button()
            
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", search_btn)
            time.sleep(1)
            search_btn.click()
            
            self.wait.until(EC.presence_of_element_located(self.RESULTS_LOCATOR))
            time.sleep(3)
            self._take_screenshot("search_results")
        except Exception as e:
            self._take_screenshot("search_error")
            raise Exception(f"Ошибка при выполнении поиска: {str(e)}")

    @allure.step("Получить заголовки результатов")
    def get_results_titles(self) -> list:
        try:
            titles = self.wait.until(
                EC.presence_of_all_elements_located(self.FILM_TITLES)
            )
            return [title.text for title in titles]
        except Exception as e:
            self._take_screenshot("get_titles_error")
            raise Exception(f"Ошибка при получении заголовков: {str(e)}")

    def _fill_mandatory_fields(self) -> None:
        """Заполнение обязательных полей, если кнопка поиска неактивна"""
        # Здесь должна быть реализация заполнения обязательных полей
        pass
