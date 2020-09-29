import time

import pytest
from selenium import webdriver

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

t_e = 5
count_products = 0


@pytest.fixture(scope="session")
def driver(request):
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    wd = webdriver.Chrome(options=options)
    request.addfinalizer(wd.quit)
    return wd


def test_login(driver):
    driver.get("http://localhost/litecart/admin/")
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()
    assert WebDriverWait(driver, t_e).until(
        EC.presence_of_element_located((By.XPATH, ".//a[@title='Logout']")))


def test_click_catalog(driver):
    catalog = driver.find_element_by_xpath(
        ".//li[@id='app-']//span[text()='Catalog']")
    time.sleep(1)
    catalog.click()
    WebDriverWait(driver, t_e).until(
        EC.presence_of_element_located(
            (By.XPATH, ".//a[text()=' Add New Product']")))
    driver.find_element_by_xpath(".//a[text()='Rubber Ducks']").click()
    WebDriverWait(driver, t_e).until(EC.url_contains("&category_id=1"))


def test_get_count_products(driver):
    global count_products
    table = driver.find_elements_by_xpath(".//table[@class='dataTable']//tr")
    rows = table[4:-1]
    count_products = int(len(rows))

    footer = table[-1].find_element_by_xpath(".//td").text
    counter = int(footer.split(" | ")[1].split("Products: ")[1])
    assert count_products == counter
    print("\nКоличество продуктов = " + str(count_products))


def test_open_product(driver, index=0):
    table = driver.find_elements_by_xpath(
        ".//table[@class='dataTable']//tr")
    rows = table[4:-1]
    columns = rows[index].find_elements_by_xpath(".//td")
    link = columns[2].find_element_by_xpath(".//a")
    time.sleep(1)
    link.click()
    WebDriverWait(driver, t_e).until(
        EC.presence_of_element_located((By.XPATH, ".//a[text()='General']")))


def test_check_log(driver, index=0):
    print("\nНомер продукта: " + str(index))
    log = driver.get_log("browser")
    for line in log:
        print(line)
    assert len(log) == 0


def test_click_cancel_button(driver):
    cancel_button = driver.find_element_by_xpath(".//button[@name='cancel']")
    time.sleep(1)
    cancel_button.click()
    WebDriverWait(driver, t_e).until(EC.presence_of_element_located(
        (By.XPATH, ".//a[text()=' Add New Product']")))


def test_open_all_product(driver):
    global count_products
    for i in range(1, count_products):
        test_open_product(driver, i)
        test_check_log(driver, i)
        test_click_cancel_button(driver)
