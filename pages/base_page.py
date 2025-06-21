from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import allure


class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.base_url = "https://www.kinopoisk.ru"
        self.wait = WebDriverWait(driver, 15)

    def open(self, path=''):
        """Открытие страницы"""
        url = f"{self.base_url}{path}"
        with allure.step(f"Открываем страницу {url}"):
            self.driver.get(url)
            self.wait_for_page_loaded()
            self.handle_cookies()

    def wait_for_page_loaded(self, timeout=15):
        """Ожидание загрузки страницы"""
        try:
            self.wait.until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )
        except TimeoutException:
            raise Exception(f"Страница не загрузилась за {timeout} секунд")

    def handle_cookies(self):
        """Обработка куки-уведомления"""
        try:
            cookie_btn = (By.XPATH, "//button[contains(., 'Принимаю')]")
            self.click_element(cookie_btn, timeout=3)
        except:
            pass

    def find_element(self, locator, timeout=15):
        """Поиск элемента с ожиданием"""
        try:
            return self.wait.until(
                EC.visibility_of_element_located(locator),
                message=f"Не найден элемент по локатору: {locator}"
            )
        except TimeoutException:
            raise NoSuchElementException(f"Элемент {locator} не найден за {timeout} сек")

    def find_elements(self, locator, timeout=15):
        """Поиск нескольких элементов"""
        try:
            return self.wait.until(
                EC.presence_of_all_elements_located(locator),
                message=f"Не найдены элементы по локатору: {locator}"
            )
        except TimeoutException:
            return []

    def is_element_present(self, locator, timeout=5):
        """Проверка наличия элемента"""
        try:
            self.find_element(locator, timeout)
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def click_element(self, locator, timeout=15):
        """Клик по элементу с ожиданием"""
        try:
            element = self.wait.until(
                EC.element_to_be_clickable(locator),
                message=f"Элемент не кликабелен: {locator}"
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.5)  # Небольшая задержка для стабильности
            element.click()
        except Exception as e:
            self._take_screenshot("click_error")
            raise Exception(f"Ошибка при клике на элемент {locator}: {str(e)}")

    def fill_field(self, locator, text, timeout=15):
        """Заполнение поля текстом"""
        element = self.find_element(locator, timeout)
        element.clear()
        element.send_keys(text)

    def _take_screenshot(self, name):
        """Создание скриншота"""
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name=name,
            attachment_type=allure.attachment_type.PNG
        )

    def wait_for_invisibility(self, locator, timeout=15):
        """Ожидание исчезновения элемента"""
        self.wait.until(
            EC.invisibility_of_element_located(locator),
            message=f"Элемент не исчез за {timeout} сек: {locator}"
        )

    def get_current_url(self):
        """Получение текущего URL"""
        return self.driver.current_url
