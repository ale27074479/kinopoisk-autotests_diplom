import allure
import pytest
import json
from helpers.api_client import KinopoiskAPIClient

@allure.feature('API Тесты Кинопоиска')
class TestKinopoiskAPI:
    client = KinopoiskAPIClient()

    @allure.story('Поиск фильма')
    @allure.title('Успешный поиск фильма по названию')
    def test_search_movie_by_title(self):
        with allure.step('Выполнить поиск фильма "Матрица"'):
            response = self.client.search_movie('Матрица')
        
        with allure.step('Проверить статус код и наличие результатов'):
            assert response.status_code == 200
            data = response.json()
            assert 'docs' in data
            assert len(data['docs']) > 0

    @allure.story('Поиск фильма')
    @allure.title('Поиск фильма с пустым запросом')
    def test_search_movie_empty_query(self):
        with allure.step('Выполнить поиск с пустым запросом'):
            response = self.client.search_movie('')
        
        with allure.step('Проверить статус код'):
            assert response.status_code in [200, 400]
            if response.status_code == 400:
                assert 'query' in response.json().get('message', '')

    @allure.story('Поиск фильма')
    @allure.title('Поиск фильма по жанру и диапазону годов')
    def test_search_movie_by_genre_and_years_range(self):
        with allure.step('Выполнить поиск комедий 2010-2020 годов'):
            response = self.client.get_movies_by_filters(
                genre='комедия',
                years_range=(2010, 2020))
        
        with allure.step('Проверить статус код'):
            assert response.status_code == 200
            data = response.json()
            if 'docs' in data and len(data['docs']) > 0:
                for movie in data['docs']:
                    assert 2010 <= movie.get('year', 0) <= 2020
            else:
                pytest.skip("Нет результатов для данных фильтров")

    @allure.story('Поиск фильма')
    @allure.title('Поиск фильма по жанру и году выпуска')
    def test_search_movie_by_genre_and_year(self):
        with allure.step('Выполнить поиск фантастики 1999 года'):
            response = self.client.get_movies_by_filters(
                genre='фантастика',
                year=1999)
        
        with allure.step('Проверить статус код'):
            assert response.status_code == 200
            data = response.json()
            if 'docs' in data and len(data['docs']) > 0:
                for movie in data['docs']:
                    assert movie.get('year') == 1999
            else:
                pytest.skip("Нет результатов для данных фильтров")

    @allure.story('Поиск персоны')
    @allure.title('Поиск актера по ID')
    def test_search_person_by_id(self):
        with allure.step('Выполнить поиск актера с ID 6317'):
            response = self.client.get_person_by_id(6317)
        
        with allure.step('Проверить статус код и данные'):
            assert response.status_code == 200
            person = response.json()
            assert 'name' in person
            assert 'enName' in person

    @allure.story('Поиск фильма')
    @allure.title('Поиск фильма по неверному ID')
    def test_search_movie_by_invalid_id(self):
        with allure.step('Выполнить поиск фильма с неверным ID'):
            response = self.client.get_movie_by_id('invalid_id')
        
        with allure.step('Проверить статус код'):
            assert response.status_code in [400, 404, 500]

    @allure.story('Поиск фильма')
    @allure.title('Поиск фильма без токена')
    def test_search_movie_without_token(self):
        with allure.step('Выполнить поиск без токена авторизации'):
            original_token = self.client.headers.pop('X-API-KEY', None)
            try:
                response = self.client.search_movie('Матрица')
                assert response.status_code == 401
                
                # Проверяем разные форматы ошибок
                response_data = response.json()
                error_message = str(response_data).lower()
                assert any(word in error_message 
                         for word in ['token', 'unauthorized', 'auth', 'key', 'доступ'])
            finally:
                if original_token:
                    self.client.headers['X-API-KEY'] = original_token
