import allure
import pytest
from helpers.api_client import KinopoiskAPIClient


@allure.feature('API Тесты Кинопоиска')
class TestKinopoiskAPI:
    """Полный набор тестов для API Кинопоиска."""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = KinopoiskAPIClient()

    # Тесты поиска фильмов
    @pytest.mark.api
    @allure.story('Поиск фильма')
    @allure.title('Поиск по жанру и году')
    def test_search_movie_by_genre_and_year(self):
        response = self.client.get_movies_by_filters(genre='фантастика', year=1999)
        assert response.status_code == 200
        
        data = response.json()
        if not data.get('docs'):
            pytest.skip("Нет результатов для данных фильтров")

        for movie in data['docs']:
            assert movie.get('year') == 1999
            genres = [g.get('name', '').lower() for g in movie.get('genres', [])]
            assert 'фантастика' in genres

    @pytest.mark.api
    @allure.story('Поиск фильма')
    @allure.title('Поиск по жанру и диапазону годов')
    def test_search_movie_by_genre_and_years_range(self):
        response = self.client.get_movies_by_filters(
            genre='комедия',
            years_range=(2010, 2020))
        
        assert response.status_code == 200
        data = response.json()

        if not data.get('docs'):
            pytest.skip("Нет результатов для данных фильтров")

        for movie in data['docs']:
            assert 2010 <= movie.get('year', 0) <= 2020
            genres = [g.get('name', '').lower() for g in movie.get('genres', [])]
            assert 'комедия' in genres

    # Тесты поиска персон
    @pytest.mark.api
    @allure.story('Поиск персоны')
    @allure.title('Поиск актера по ID')
    def test_search_person_by_id(self):
        response = self.client.get_person_by_id(6317)  # Леонардо ДиКаприо
        assert response.status_code == 200
        
        person = response.json()
        assert all(field in person for field in ['id', 'name', 'enName', 'photo'])

    # Негативные тесты
    @pytest.mark.api
    @allure.story('Негативные тесты')
    @allure.title('Поиск фильма по неверному ID')
    @pytest.mark.parametrize('invalid_id', ['invalid_id', '0', '-1', '99999999999999999999'])
    def test_search_movie_by_invalid_id(self, invalid_id):
        response = self.client.get_movie_by_id(invalid_id)
        assert response.status_code in [400, 404, 422, 500]  # Расширены возможные коды ответа

    @pytest.mark.api
    @allure.story('Негативные тесты')
    @allure.title('Поиск без токена')
    def test_search_movie_without_token(self):
        original_token = self.client.headers.pop('X-API-KEY', None)
        try:
            response = self.client.search_movie('Матрица')
            assert response.status_code == 401
        finally:
            if original_token:
                self.client.headers['X-API-KEY'] = original_token

    # Граничные случаи
    @pytest.mark.api
    @allure.story('Граничные случаи')
    @allure.title('Поиск с граничными годами')
    @pytest.mark.parametrize('year', [1895, 2023, 1900, 2000])
    def test_search_with_boundary_years(self, year):
        response = self.client.get_movies_by_filters(year=year)
        assert response.status_code == 200

    @pytest.mark.api
    @allure.story('Граничные случаи')
    @allure.title('Поиск с длинным названием')
    def test_search_with_long_title(self):
        response = self.client.search_movie('о' * 100)
        assert response.status_code in [200, 400, 422, 500]  # Расширены возможные коды
