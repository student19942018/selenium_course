import pytest
from selenium import webdriver


@pytest.fixture
def driver(request):
    BROWSERSTACK_URL = 'https://bsuser7502154730:VpQXNd9JRPPApStAq8Bv@hub-cloud.browserstack.com/wd/hub'

    desired_cap = {

        'os': 'Windows',
        'os_version': '10',
        'browser': 'Chrome',
        'browser_version': '80',
        'name': "bsuser7502154730's First Test"

    }

    wd = webdriver.Remote(
        command_executor=BROWSERSTACK_URL,
        desired_capabilities=desired_cap
    )
    request.addfinalizer(wd.quit)
    return wd


def test_example(driver):
    driver.get("http://www.google.com")
    if not "Google" in driver.title:
        raise Exception("Unable to load google page!")
    elem = driver.find_element_by_name("q")
    elem.send_keys("BrowserStack")
    elem.submit()
    print(driver.title)