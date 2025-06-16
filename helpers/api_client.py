import os
import requests
from dotenv import load_dotenv

load_dotenv()

class KinopoiskAPIClient:
    def __init__(self):
        self.base_url = os.getenv('KINOPOISK_API_URL', 'https://api.kinopoisk.dev')
        self.token = os.getenv('KINOPOISK_API_TOKEN')
        self.headers = {'X-API-KEY': self.token} if self.token else {}
        self.timeout = 10
    
    def search_movie(self, query):
        url = f"{self.base_url}/v1.2/movie/search"
        params = {'query': query, 'limit': 5}
        return requests.get(url, headers=self.headers, params=params, timeout=self.timeout)
    
    def get_movie_by_id(self, movie_id):
        url = f"{self.base_url}/v1.3/movie/{movie_id}"
        return requests.get(url, headers=self.headers, timeout=self.timeout)
    
    def get_movies_by_filters(self, genre=None, year=None, years_range=None):
        url = f"{self.base_url}/v1.3/movie"
        params = {'limit': 5}
        if genre:
            params['genres.name'] = genre
        if year:
            params['year'] = year
        if years_range:
            params['years.start'] = years_range[0]
            params['years.end'] = years_range[1]
        return requests.get(url, headers=self.headers, params=params, timeout=self.timeout)
    
    def get_person_by_id(self, person_id):
        url = f"{self.base_url}/v1/person/{person_id}"
        return requests.get(url, headers=self.headers, timeout=self.timeout)
