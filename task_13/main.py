import time
from functools import reduce

import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import Select

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

products = {}
t_e = 5


def add_product(new_product):
    global products
    count = products.get(new_product, 0)    # вернёт 0, если данного ключа нет
    if count:
        products[new_product] += 1
    else:
        products[new_product] = 1


def is_element_present(driver, locator):
    return len(driver.find_elements_by_xpath(locator)) > 0


@pytest.fixture(scope="session")
def driver(request):
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    wd = webdriver.Chrome(options=options)
    request.addfinalizer(wd.quit)
    return wd


def test_open_main_page_driver(driver):
    driver.get("http://localhost/litecart/en/")
    assert WebDriverWait(driver, t_e).until(EC.title_is("Online Store | My Store"))


def test_click_product(driver):
    first_product = driver.find_elements_by_xpath(".//li[contains(@class, 'product')]")[0]
    name = first_product.find_element_by_xpath(".//div[@class='name']").text
    add_product(name)
    first_product.find_element_by_xpath(".//a[@class='link']").click()
    h1 = WebDriverWait(driver, t_e).until(EC.presence_of_element_located((By.XPATH, ".//h1")))
    assert h1.text == name


def test_add_to_cart(driver):
    locator_counter = ".//span[@class='quantity']"
    count_items = int(driver.find_element_by_xpath(locator_counter).text)

    if is_element_present(driver, ".//select[@name='options[Size]']"):
        select = Select(driver.find_element_by_xpath(".//select[@name='options[Size]']"))
        select.select_by_index(1)   # выбираем первый имеющийся размер

    time.sleep(1)
    driver.find_element_by_xpath(".//button[@name='add_cart_product']").click()

    WebDriverWait(driver, t_e).until(EC.text_to_be_present_in_element((By.XPATH, locator_counter), str(count_items + 1)))


def test_back_to_main_page(driver):
    driver.find_element_by_xpath(".//div[@id='logotype-wrapper']//a").click()
    assert WebDriverWait(driver, t_e).until(EC.title_is("Online Store | My Store"))


def test_add_two_products(driver):
    global products
    for _ in range(2):
        test_click_product(driver)
        test_add_to_cart(driver)
        test_back_to_main_page(driver)

    assert reduce(lambda x, y: x+y, products.values()) == 3


def test_open_cart(driver):
    time.sleep(1)
    driver.find_element_by_xpath(".//div[@id='cart']//a[text()='Checkout »']").click()
    assert WebDriverWait(driver, t_e).until(EC.title_is("Checkout | My Store"))


def test_delete_product(driver):
    global products
    rows = driver.find_elements_by_xpath(".//table[@class='dataTable rounded-corners']//td[@class='item']//parent::tr")
    assert len(rows) == len(products)
    print("\n Кол-во строк в таблице и элементов в products совпадает = {}".format(len(rows)))

    if is_element_present(driver, ".//li[@class='shortcut']"):
        shortcuts = driver.find_elements_by_xpath(".//li[@class='shortcut']")
        print("Число карточек в Превью = {}".format(len(shortcuts)))
        shortcuts[0].find_element_by_xpath(".//a").click()

    viewport_product = driver.find_element_by_xpath(".//li[@class='item']")
    name_product = viewport_product.find_element_by_xpath(".//strong").text
    quantity_product = int(rows[0].find_elements_by_xpath(".//td")[0].text)
    assert products[name_product] == quantity_product

    print(products)
    print(name_product)

    delete_button = viewport_product.find_element_by_xpath(".//button[@name='remove_cart_item']")
    time.sleep(1)
    delete_button.click()
    WebDriverWait(driver, t_e).until(EC.staleness_of(rows[0]))
    
    products.pop(name_product)
    print(products)


def test_clear_cart(driver):
    global products
    while len(products) > 0:
        test_delete_product(driver)
    WebDriverWait(driver, t_e).until(EC.text_to_be_present_in_element((By.XPATH, ".//em"), "There are no items in your cart."))
