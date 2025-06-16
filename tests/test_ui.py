import os
import allure
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from pages.main_page import MainPage
from pages.search_page import SearchPage
from pages.movies_page import MoviesPage
from pages.advanced_search_page import AdvancedSearchPage

load_dotenv()

@pytest.fixture(scope='function')
def driver():
    options = webdriver.ChromeOptions()
    if os.getenv('HEADLESS') == 'True':
        options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()

@allure.feature('UI Тесты Кинопоиска')
class TestKinopoiskUI:
    @allure.story('Поиск фильма')
    @allure.title('Поиск существующего фильма')
    def test_search_existing_movie(self, driver):
        main_page = MainPage(driver)
        search_page = SearchPage(driver)
        
        main_page.open()
        main_page.accept_cookies()
        main_page.search_movie('Интерстеллар')
        assert len(search_page.get_search_results()) > 0

    @allure.story('Поиск фильма')
    @allure.title('Поиск несуществующего фильма')
    def test_search_non_existing_movie(self, driver):
        main_page = MainPage(driver)
        search_page = SearchPage(driver)
        
        main_page.open()
        main_page.accept_cookies()
        main_page.search_movie('несуществующийфильм123')
        assert search_page.is_no_results()

    @allure.story('Фильтрация')
    @allure.title('Фильтрация по жанру')
    def test_filter_by_genre(self, driver):
        movies_page = MoviesPage(driver)
        movies_page.open()
        movies_page.accept_cookies()
        movies_page.open_genre_filter()
        movies_page.select_genre('комедия')
        assert len(movies_page.get_movie_titles()) > 0

    @allure.story('Фильтрация')
    @allure.title('Фильтрация по году')
    def test_filter_by_year(self, driver):
        movies_page = MoviesPage(driver)
        movies_page.open()
        movies_page.accept_cookies()
        movies_page.open_year_filter()
        movies_page.select_year('2020')
        assert len(movies_page.get_movie_titles()) > 0

    @allure.story('Расширенный поиск')
    @allure.title('Поиск с фильтрами')
    def test_advanced_search(self, driver):
        main_page = MainPage(driver)
        advanced_search = AdvancedSearchPage(driver)
        
        main_page.open()
        main_page.accept_cookies()
        main_page.go_to_advanced_search()
        
        advanced_search.set_year_range(2010, 2020)
        advanced_search.select_genre('фантастика')
        advanced_search.submit_search()
        
        assert len(advanced_search.get_results()) > 0
