import pytest
from selenium import webdriver
from dotenv import load_dotenv
import os

load_dotenv()


def pytest_addoption(parser):
    parser.addoption('--browser', action='store', default='chrome',
                    help='Choose browser: chrome or firefox')
    parser.addoption('--headless', action='store_true',
                    help='Run tests in headless mode')


@pytest.fixture(scope='function')
def driver(request):
    browser = request.config.getoption('browser')
    headless = request.config.getoption('headless')
    
    if browser == 'chrome':
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
    elif browser == 'firefox':
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument('--headless')
        driver = webdriver.Firefox(options=options)
    else:
        raise ValueError(f'Unsupported browser: {browser}')
    
    driver.maximize_window()
    yield driver
    driver.quit()
