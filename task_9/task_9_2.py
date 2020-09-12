import pytest
from selenium import webdriver

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


@pytest.fixture(scope="session")
def driver(request):
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    wd = webdriver.Chrome(chrome_options=options)
    request.addfinalizer(wd.quit)
    return wd


def test_login(driver):
    driver.get("http://localhost/litecart/admin/?app=geo_zones&doc=geo_zones")
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()
    WebDriverWait(driver, 5).\
        until(EC.presence_of_element_located((By.XPATH, ".//h1")))


def test_sorted_zones(driver):
    rows_countries = driver.find_elements_by_xpath(".//tr[@class='row']")
    countries = []
    for row in rows_countries:
        columns = row.find_elements_by_xpath(".//td")
        link = columns[2].find_element_by_xpath("./a")
        print(link.get_attribute("href"))
        countries.append(link.get_attribute("href"))

    print("------------Check sorted zones------------")
    for country in countries:
        driver.get(country)
        WebDriverWait(driver, 5). \
            until(EC.presence_of_element_located((By.XPATH, ".//h2")))
        rows_zones = driver.find_elements_by_xpath(".//table[@id='table-zones']//tr")
        rows_zones = rows_zones[1:-1]
        zones = []
        for row in rows_zones:
            columns = row.find_elements_by_xpath(".//td")
            select = columns[2].find_element_by_xpath("./select")
            name_zone = select.find_element_by_xpath(".//option[@selected='selected']").text
            print(name_zone)
            zones.append(name_zone)
        print()
        assert sorted(zones) == zones
