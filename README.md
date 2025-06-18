# Автоматизированное тестирование Кинопоиска

Этот проект содержит автоматизированные UI и API тесты для сайта Кинопоиск.
## Настройка окружения

1. Установите Python 
2. Установите зависимости: `pip install -r requirements.txt`
3. Создайте файл `.env` в корне проекта
4. Добавьте в него переменные:
KINOPOISK_API_TOKEN=your_api_token_here
KINOPOISK_URL=https://www.kinopoisk.ru

## Структура проекта

- `pages/` - Page Object модели для работы со страницами сайта
  - `base_page.py` - базовый класс для всех страниц
  - `main_page.py` - главная страница Кинопоиска
  - `movies_page.py` - страница с фильмами
  - `search_page.py` - страница результатов поиска
  - `advanced_search_page.py` - страница расширенного поиска
- `tests/` - автоматизированные тесты
  - `test_ui.py` - UI тесты
  - `test_api.py` - API тесты
- `helpers/` - вспомогательные утилиты
 - `api_client.py` - клиент для работы с API Кинопоиска
 - `retry.py` Декоратор для повторного выполнения функции при возникновении исключений
- `.env` - файл с настройками окружения
- `conftest.py` - фикстуры pytest
- `pytest.ini` - конфигурация pytest
- `requirements.txt` - зависимости проекта

## Требования

- Python 
- Установленный Chrome или Firefox
- API токен Кинопоиска (для API тестов)
- Chrome 
- ChromeDriver соответствующей версии

## Запуск тестов

- Все тесты: `pytest`
- Только API тесты: `pytest -m api`
- Только UI тесты: `pytest -m ui`
- С отчетом: `pytest --html=report.html`


## Установка

 Клонировать репозиторий:
   ```bash
   git clone https://github.com/ale27074479/kinopoisk-autotests_diplom.git
   cd kinopoisk-autotests_diplom