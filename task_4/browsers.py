import pytest
from selenium import webdriver
from msedge.selenium_tools import Edge, EdgeOptions


@pytest.fixture
def driver(request):
    # старая схема запуска Firefox:
    # options = webdriver.FirefoxOptions()
    # options.binary_location = "C:\\Program Files\\Mozilla Firefox ESR\\firefox.exe"
    # wd = webdriver.Firefox(capabilities={"marionette": False}, options=options)

    # запуск Firefox Nightly:
    # options = webdriver.FirefoxOptions()
    # options.binary_location = "C:\\Program Files\Firefox Nightly\\firefox.exe"
    # wd = webdriver.Firefox(options=options)

    # запуск Firefox (альтернативный вариант указания пути):
    wd = webdriver.Firefox(firefox_binary="C:\\Program Files\Mozilla Firefox\\firefox.exe")

    # Microsoft Edge (based on Chromium)
    # https://github.com/microsoft/edge-selenium-tools
    # https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
    # options = EdgeOptions()
    # options.use_chromium = True
    # wd = Edge(options=options, capabilities={"unexpectedAlertBehaviour": "dismiss"})
    # print(wd.capabilities)

    request.addfinalizer(wd.quit)
    return wd


def test_example(driver):
    driver.get("http://localhost/litecart/admin/")
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()
