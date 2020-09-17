import time
from datetime import datetime, timedelta
from pathlib import Path
import random
import string

import pytest

from selenium import webdriver
from selenium.webdriver.support.ui import Select

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


name = ''


def generate_date(days_delta=0, pattern='%d.%m.%Y'):
    return (datetime.today() + timedelta(days=days_delta)).strftime(pattern)


def generate_random_string(length):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))


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


def test_click_catalog(driver):
    catalog = driver.find_element_by_xpath(".//span[text()='Catalog']//parent::a")
    time.sleep(1)
    catalog.click()
    WebDriverWait(driver, 5).until(EC.presence_of_element_located(
        (By.XPATH, ".//a[text()=' Add New Product']")))


def test_click_add_new_product(driver):
    driver.find_element_by_xpath(".//a[text()=' Add New Product']").click()
    WebDriverWait(driver, 5).until(EC.presence_of_element_located(
        (By.XPATH, ".//h1[text()=' Add New Product']")))


def test_fill_general(driver):
    global name
    current_time = generate_date(pattern="%H-%M-%S.%d-%b-%Y")
    name = "Name " + current_time
    time.sleep(1)

    driver.find_element_by_xpath(".//input[@name='status']").click()
    driver.find_element_by_xpath(".//input[@name='name[en]']").send_keys(name)
    driver.find_element_by_xpath(".//input[@name='code']").send_keys("Code" + current_time)

    categories = driver.find_elements_by_xpath(".//input[@name='categories[]']")
    for x in categories[1:]:
        x.click()

    default_category = Select(driver.find_element_by_xpath(".//select[@name='default_category_id']"))
    index = random.randint(0, len(default_category.options) - 1)
    default_category.select_by_index(index)

    groups = driver.find_elements_by_xpath(".//input[@name='product_groups[]']")
    groups[random.randint(0, len(groups) - 1)].click()

    quantity = driver.find_element_by_xpath(".//input[@name='quantity']")
    quantity.clear()
    quantity.send_keys(str(random.randint(1, 1000)))

    sold_out_status = Select(driver.find_element_by_xpath(".//select[@name='sold_out_status_id']"))
    sold_out_status.select_by_visible_text("Temporary sold out")

    image = driver.find_element_by_xpath(".//input[@name='new_images[]']")
    path = str(Path.cwd() / 'cat.jpg')
    image.send_keys(path)

    date_valid_from = driver.find_element_by_xpath(".//input[@name='date_valid_from']")
    date_valid_from.send_keys(generate_date())

    date_valid_to = driver.find_element_by_xpath(".//input[@name='date_valid_to']")
    date_valid_to.send_keys(generate_date(30))


def test_click_information(driver):
    driver.find_element_by_xpath(".//a[text()='Information']").click()


def test_fill_information(driver):
    time.sleep(1)

    manufacturer = Select(driver.find_element_by_xpath(".//select[@name='manufacturer_id']"))
    manufacturer.select_by_visible_text("ACME Corp.")

    keyword = driver.find_element_by_xpath(".//input[@name='keywords']")
    keyword.send_keys("keyword: " + generate_random_string(5))

    short_description = driver.find_element_by_xpath(".//input[@name='short_description[en]']")
    short_description.send_keys("Short Description: " + generate_random_string(10))

    description = driver.find_element_by_xpath(".//div[@class='trumbowyg-editor']")
    description.send_keys("Description: " + generate_random_string(100))

    head_title = driver.find_element_by_xpath(".//input[@name='head_title[en]']")
    head_title.send_keys("Head Title: " + generate_random_string(10))

    meta_description = driver.find_element_by_xpath(".//input[@name='meta_description[en]']")
    meta_description.send_keys("Meta Description: " + generate_random_string(5))


def test_click_prices(driver):
    driver.find_element_by_xpath(".//a[text()='Prices']").click()


def test_fill_prices(driver):
    time.sleep(1)

    purchase_price = driver.find_element_by_xpath(".//input[@name='purchase_price']")
    purchase_price.clear()
    price = random.randint(1, 1000)
    purchase_price.send_keys(str(price))

    purchase_price = Select(driver.find_element_by_xpath(".//select[@name='purchase_price_currency_code']"))
    purchase_price.select_by_visible_text("US Dollars")

    prices_usd = driver.find_element_by_xpath(".//input[@name='prices[USD]']")
    prices_usd.send_keys(str(round(price * 1.4)))

    prices_eur = driver.find_element_by_xpath(".//input[@name='prices[EUR]']")
    prices_eur.send_keys(str(round(price * 1.2)))


def test_click_save(driver):
    driver.find_element_by_xpath(".//button[@name='save']").click()
    WebDriverWait(driver, 5).until(EC.presence_of_element_located, (By.XPATH, ".//h1[text()=' Catalog']"))


def test_check_save(driver):
    time.sleep(2)
    driver.find_element_by_xpath(".//a[text()='Rubber Ducks']").click()
    WebDriverWait(driver, 5).until(EC.presence_of_element_located, (By.XPATH, ".//a[text()='Subcategory']"))
    driver.find_element_by_xpath(".//a[text()='Subcategory']").click()
    products = driver.find_elements_by_xpath(".//a[text()='{}']".format(name))
    assert len(products) == 3
