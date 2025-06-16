# Автоматизированное тестирование Кинопоиска

Этот проект содержит автоматизированные UI и API тесты для сайта Кинопоиск.

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
- `.env` - файл с настройками окружения
- `conftest.py` - фикстуры pytest
- `pytest.ini` - конфигурация pytest
- `requirements.txt` - зависимости проекта

## Требования

- Python 
- Установленный Chrome или Firefox
- API токен Кинопоиска (для API тестов)

## Установка

1. Клонировать репозиторий:
   ```bash
   git clone https://github.com/ale27074479/kinopoisk-autotests_diplom.git
   cd kinopoisk-autotests_diplom