import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.main_page import MainPage
from pages.search_page import SearchPage
from pages.movies_page import MoviesPage
from pages.advanced_search_page import AdvancedSearchPage

@pytest.mark.ui
@allure.feature("UI Тесты Кинопоиска")
class TestKinopoiskUI:
    @allure.story("Поиск фильма")
    @allure.title("Поиск существующего фильма")
    def test_search_existing_movie(self, driver):
        """Проверка поиска существующего фильма."""
        main_page = MainPage(driver)
        main_page.open()
        
        try:
            main_page.accept_cookies()
        except:
            pass
            
        search_page = main_page.search_movie("Интерстеллар")
        results = search_page.get_search_results()
        
        assert len(results) > 0, "Не найдены результаты поиска"
        assert any("интерстеллар" in movie.text.lower() for movie in results), "Не найден искомый фильм"

    @allure.story("Поиск фильма")
    @allure.title("Поиск несуществующего фильма")
    def test_search_nonexistent_movie(self, driver):
        """Проверка отображения сообщения при отсутствии результатов."""
        main_page = MainPage(driver)
        main_page.open()
        
        search_page = main_page.search_movie("НесуществующийФильм12345абвгд")
        no_results = search_page.is_no_results()
        
        assert no_results, "Не отображается сообщение об отсутствии результатов"

    @allure.story("Фильтрация фильмов")
    @allure.title("Фильтрация по жанру")
    def test_filter_movies_by_genre(self, driver):
        """Проверка фильтрации фильмов по жанру."""
        movies_page = MoviesPage(driver)
        movies_page.open("/lists/movies/top250/")
        
        try:
            movies_page.accept_cookies()
        except:
            pass
            
        movies_page.open_genre_filter()
        movies_page.select_genre("комедия")
        
        movie_titles = movies_page.get_movie_titles()
        assert len(movie_titles) > 0, "Не найдены фильмы после фильтрации"

    @allure.story("Расширенный поиск")
    @allure.title("Расширенный поиск по году и жанру")
    def test_advanced_search_by_year_and_genre(self, driver):
        """Проверка расширенного поиска с фильтрами."""
        main_page = MainPage(driver)
        main_page.open("/s/")
        
        try:
            main_page.accept_cookies()
        except:
            pass
            
        advanced_search_page = AdvancedSearchPage(driver)
        advanced_search_page.set_year_range(2010, 2020)
        advanced_search_page.select_genre("фантастика")
        advanced_search_page.submit_search()
        
        results = advanced_search_page.get_results()
        assert len(results) > 0, "Не найдены фильмы по заданным критериям"

    @allure.story("Основная функциональность")
    @allure.title("Проверка главной страницы")
    def test_main_page_content(self, driver):
        """Проверка основных элементов на главной странице."""
        main_page = MainPage(driver)
        main_page.open()
        
        try:
            main_page.accept_cookies()
        except:
            pass
            
        search_field = main_page.find_element(main_page.SEARCH_FIELD)
        search_button = main_page.find_element(main_page.SEARCH_BUTTON)
        
        assert search_field.is_displayed(), "Поле поиска не отображается"
        assert search_button.is_displayed(), "Кнопка поиска не отображается"
