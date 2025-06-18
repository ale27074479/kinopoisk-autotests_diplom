import allure
import pytest
from helpers.api_client import KinopoiskAPIClient


@allure.feature('API Тесты Кинопоиска')
class TestKinopoiskAPI:
    """Тесты для API Кинопоиска."""
    
    client = KinopoiskAPIClient()
    @pytest.mark.api
    @allure.story('Поиск фильма')
    @allure.title('Поиск фильма по жанру и году выпуска')
    def test_search_movie_by_genre_and_year(self):
        """Тест поиска по жанру и конкретному году."""
        with allure.step('Выполнить поиск фантастики 1999 года'):
            try:
                response = self.client.get_movies_by_filters(
                    genre='фантастика',
                    year=1999)
            except Exception as e:
                pytest.fail(f"Ошибка при выполнении запроса: {str(e)}")
        
        with allure.step('Проверить статус код'):
            assert response.status_code == 200
            data = response.json()
            
            if 'docs' not in data or len(data['docs']) == 0:
                pytest.skip("Нет результатов для данных фильтров")
            
            for movie in data['docs']:
                assert movie.get('year') == 1999
                # Более надежная проверка жанра
                movie_genres = [g.get('name', '').lower() for g in movie.get('genres', [])]
                assert 'фантастика' in movie_genres
    @pytest.mark.api
    @allure.story('Поиск фильма')
    @allure.title('Поиск фильма по жанру и диапазону годов')
    def test_search_movie_by_genre_and_years_range(self):
        """Тест поиска по жанру и диапазону годов."""
        with allure.step('Выполнить поиск комедий 2010-2020 годов'):
            try:
                response = self.client.get_movies_by_filters(
                    genre='комедия',
                    years_range=(2010, 2020))
            except Exception as e:
                pytest.fail(f"Ошибка при выполнении запроса: {str(e)}")
        
        with allure.step('Проверить статус код'):
            assert response.status_code == 200
            data = response.json()
            
            if 'docs' not in data or len(data['docs']) == 0:
                pytest.skip("Нет результатов для данных фильтров")
            
            for movie in data['docs']:
                assert 2010 <= movie.get('year', 0) <= 2020
                # Более надежная проверка жанра
                movie_genres = [g.get('name', '').lower() for g in movie.get('genres', [])]
                assert 'комедия' in movie_genres or 'комедийный' in movie_genres
    
    @pytest.mark.api
    @allure.story('Поиск персоны')
    @allure.title('Поиск актера по ID')
    def test_search_person_by_id(self):
        """Тест поиска актера по ID с проверкой обязательных полей."""
        with allure.step('Выполнить поиск актера с ID 6317'):
            response = self.client.get_person_by_id(6317)
        
        with allure.step('Проверить статус код и данные'):
            assert response.status_code == 200
            person = response.json()
            
            required_fields = ['id', 'name', 'enName', 'photo', 'profession']
            for field in required_fields:
                assert field in person, f'Отсутствует обязательное поле {field}'

    @pytest.mark.api
    @allure.story('Поиск фильма')
    @allure.title('Поиск фильма по неверному ID')
    def test_search_movie_by_invalid_id(self):
        """Негативный тест поиска фильма по неверному ID."""
        invalid_ids = ['', 'invalid_id', '0', '-1', None, '99999999999999999999']
        
        for invalid_id in invalid_ids:
            with allure.step(f'Выполнить поиск фильма с ID: {invalid_id}'):
                response = self.client.get_movie_by_id(invalid_id)
            
            with allure.step('Проверить статус код'):
                assert response.status_code in [400, 404, 500]
                
                if response.status_code != 500:
                    error_data = response.json()
                    assert 'message' in error_data
    @pytest.mark.api  
    @allure.story('Поиск фильма')
    @allure.title('Поиск фильма без токена')
    def test_search_movie_without_token(self):
        """Негативный тест поиска без токена авторизации."""
        with allure.step('Выполнить поиск без токена авторизации'):
            original_token = self.client.headers.pop('X-API-KEY', None)
            try:
                response = self.client.search_movie('Матрица')
                assert response.status_code == 401
                
                response_data = response.json()
                error_message = str(response_data).lower()
                assert any(word in error_message 
                         for word in ['token', 'unauthorized', 'auth', 'key', 'доступ'])
            finally:
                if original_token:
                    self.client.headers['X-API-KEY'] = original_token
    @pytest.mark.api
    @allure.story('Поиск фильма')
    @allure.title('Поиск с граничными значениями параметров')
    @pytest.mark.parametrize('year', [1895, 2023, 1900, 2000, 2100])
    def test_search_with_boundary_years(self, year):
        """Тест поиска с граничными значениями годов."""
        response = self.client.get_movies_by_filters(year=year)
        assert response.status_code == 200
        
        data = response.json()
        if 'docs' in data and len(data['docs']) > 0:
            for movie in data['docs']:
                assert 'year' in movie
                
    @pytest.mark.api
    @allure.story('Поиск фильма')
    @allure.title('Поиск с очень длинным названием')
    def test_search_with_long_title(self):
        """Тест поиска с очень длинным названием."""
        long_title = 'о' * 255
        response = self.client.search_movie(long_title)
        
        assert response.status_code in [200, 400]
        if response.status_code == 200:
            data = response.json()
            assert 'docs' in data
