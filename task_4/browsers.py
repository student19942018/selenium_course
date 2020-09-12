import pytest
from selenium import webdriver
from msedge.selenium_tools import Edge, EdgeOptions


browser = "IE"


@pytest.fixture(scope="session")
def driver(request):
    if browser == "Chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        wd = webdriver.Chrome(options=options)

    if browser == "Firefox":
        wd = webdriver.Firefox(firefox_binary="C:\\Program Files\Mozilla Firefox\\firefox.exe")

    if browser == "Firefox ESR":
        wd = webdriver.Firefox(capabilities={"marionette": False},
                               firefox_binary="C:\\Program Files\\Mozilla Firefox ESR\\firefox.exe")

    if browser == "Firefox Nightly":
        wd = webdriver.Firefox(firefox_binary="C:\\Program Files\Firefox Nightly\\firefox.exe")

    if browser == "Microsoft Edge":
    # Microsoft Edge (based on Chromium)
    # https://github.com/microsoft/edge-selenium-tools
    # https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
        options = EdgeOptions()
        options.use_chromium = True
        wd = Edge(options=options, capabilities={"unexpectedAlertBehaviour": "dismiss"})
        print(wd.capabilities)

    if browser == "IE":
        wd = webdriver.Ie(capabilities={"requireWindowFocus": True})

    request.addfinalizer(wd.quit)
    return wd


def test_example(driver):
    driver.get("http://localhost/litecart/admin/")
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()
