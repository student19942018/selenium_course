import pytest
from selenium import webdriver


@pytest.fixture
def driver(request):
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    driver = webdriver.Chrome(chrome_options=options)
    request.addfinalizer(driver.quit)
    return driver


def test_check_stickers(driver):
    driver.get("http://localhost/litecart/en/")
    products = driver.find_elements_by_xpath(".//li[contains(@class, 'product')]")
    for product in products:
        stickers = product.find_elements_by_xpath(".//div[contains(@class, 'sticker')]")
        assert len(stickers) == 1

