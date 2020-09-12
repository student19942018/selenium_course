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
    driver.get("http://localhost/litecart/admin/?app=countries&doc=countries")
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()
    WebDriverWait(driver, 5).\
        until(EC.presence_of_element_located((By.XPATH, ".//h1")))


def test_sorted_countries_and_zones(driver):
    rows_countries = driver.find_elements_by_xpath(".//tr[@class='row']")
    names_countries = []
    links_countries = []
    for row in rows_countries:
        columns = row.find_elements_by_xpath(".//td")
        link = columns[4].find_element_by_xpath("./a")
        name_country = link.text
        print(name_country)
        count_zones = int(columns[5].text)
        if count_zones > 0:
            print("\t - " + link.get_attribute("href"))
            links_countries.append(link.get_attribute("href"))
        names_countries.append(name_country)
    assert sorted(names_countries) == names_countries

    print("------------Check sorted zones------------")
    for country in links_countries:
        driver.get(country)
        WebDriverWait(driver, 5). \
            until(EC.presence_of_element_located((By.XPATH, ".//h2")))
        rows_zones = driver.find_elements_by_xpath(".//table[@id='table-zones']//tr")
        rows_zones = rows_zones[1:-1]
        zones = []
        for row in rows_zones:
            columns = row.find_elements_by_xpath(".//td")
            name_zone = columns[2].find_element_by_xpath("./input").get_attribute("value")
            print(name_zone)
            zones.append(name_zone)
        assert sorted(zones) == zones
        print()
