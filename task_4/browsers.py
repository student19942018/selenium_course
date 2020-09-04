import pytest
from selenium import webdriver
from msedge.selenium_tools import Edge, EdgeOptions


@pytest.fixture
def driver(request):
    # wd = webdriver.Firefox()

    # https://github.com/microsoft/edge-selenium-tools
    # https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
    options = EdgeOptions()
    options.use_chromium = True
    wd = Edge(options=options)

    request.addfinalizer(wd.quit)
    return wd


def test_example(driver):
    driver.get("http://localhost/litecart/admin/")
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()
