from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

BROWSERSTACK_URL = 'https://bsuser7502154730:VpQXNd9JRPPApStAq8Bv@hub-cloud.browserstack.com/wd/hub'

desired_cap = {

    'os': 'Windows',
    'os_version': '10',
    'browser': 'Chrome',
    'browser_version': '80',
    'name': "bsuser7502154730's First Test"

}

driver = webdriver.Remote(
    command_executor=BROWSERSTACK_URL,
    desired_capabilities=desired_cap
)

driver.get("http://www.google.com")
if not "Google" in driver.title:
    raise Exception("Unable to load google page!")
elem = driver.find_element_by_name("q")
elem.send_keys("BrowserStack")
elem.submit()
print(driver.title)
driver.quit()