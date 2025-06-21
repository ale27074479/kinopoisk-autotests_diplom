import allure
import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pages.main_page import MainPage
from pages.movie_page import MoviePage
from pages.advanced_search_page import AdvancedSearchPage


@allure.feature("UI Тесты Кинопоиска")
@pytest.mark.ui
def test_search_existing_movie(driver):
    """Поиск существующего фильма."""
    main_page = MainPage(driver)
    main_page.open()
    time.sleep(2)
    
    search_page = main_page.search_movie("Интерстеллар")
    time.sleep(2)
    
    assert search_page.get_search_results_count() > 0


@allure.feature("UI Тесты Кинопоиска")
@pytest.mark.ui
def test_search_nonexistent_movie(driver):
    """Поиск несуществующего фильма."""
    main_page = MainPage(driver)
    main_page.open()
    time.sleep(2)
    
    search_page = main_page.search_movie("НесуществующийФильм12345абвгд")
    time.sleep(2)
    
    assert search_page.is_no_results()


@allure.feature("UI Тесты Кинопоиска")
@pytest.mark.ui
def test_main_page_elements(driver):
    """Проверка элементов главной страницы."""
    main_page = MainPage(driver)
    main_page.open()
    time.sleep(2)
    
    assert main_page.is_element_present(MainPage.SEARCH_FIELD)
    assert main_page.is_element_present(MainPage.SEARCH_BUTTON)


@allure.feature("UI Тесты Кинопоиска")
@pytest.mark.ui
def test_movie_page_rating(driver):
    """Проверка отображения рейтинга на странице фильма."""
    with allure.step("Открыть страницу фильма"):
        movie_page = MoviePage(driver)
        movie_page.open("/film/326/")  # Побег из Шоушенка
        time.sleep(3)
    
    with allure.step("Принять куки, если есть"):
        try:
            accept_btn = (By.XPATH, "//button[contains(., 'Принимаю')]")
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable(accept_btn)).click()
        except:
            pass
    
    with allure.step("Прокрутить к рейтингу"):
        driver.execute_script("window.scrollTo(0, 500)")
        time.sleep(2)
    
    with allure.step("Проверить отображение рейтинга"):
        assert movie_page.is_rating_displayed(), "Рейтинг фильма не отображается"
        rating = movie_page.get_movie_rating()
        assert rating > 0, f"Некорректное значение рейтинга: {rating}"


@allure.feature("UI Тесты Кинопоиска")
@pytest.mark.ui
def test_advanced_search_by_keyword(driver):
    """Проверка расширенного поиска по ключевому слову."""
    search_page = AdvancedSearchPage(driver)
    
    with allure.step("1. Открыть страницу расширенного поиска"):
        search_page.driver.get("https://www.kinopoisk.ru/s/")
        time.sleep(5)
        search_page._take_screenshot("page_loaded")
    
    with allure.step("2. Принять куки, если есть"):
        search_page.accept_cookies()
    
    with allure.step("3. Ввести ключевое слово 'космос'"):
        search_page.search_by_keyword("космос")
        time.sleep(2)
    
    with allure.step("4. Выполнить поиск"):
        search_page.perform_search()
        time.sleep(5)
    
    with allure.step("5. Проверить результаты поиска"):
        titles = search_page.get_results_titles()
        assert len(titles) > 0, "Не найдены фильмы по ключевому слову 'космос'"
        
        allure.attach(
            "\n".join(titles[:5]),
            name="Первые 5 результатов",
            attachment_type=allure.attachment_type.TEXT
        )
