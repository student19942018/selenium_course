import time
import random
import string
from functools import reduce

import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import Select

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

email = ''
password = ''


def get_random_string_of_numbers(length):
    digits = random.sample([int(x) for x in string.digits], length)
    return reduce(lambda x, y: str(x) + str(y), digits)


@pytest.fixture(scope="session")
def driver(request):
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    wd = webdriver.Chrome(options=options)

    request.addfinalizer(wd.quit)
    return wd


def test_open_main_page(driver):
    driver.get("http://localhost/litecart/en/")
    WebDriverWait(driver, 5).until(EC.presence_of_element_located, (By.XPATH, ".//button[@name='login']"))


def test_click_new_customers(driver):
    link = driver.find_element_by_xpath(".//form[@name='login_form']//a")
    link.click()
    WebDriverWait(driver, 5).until(EC.presence_of_element_located, (By.XPATH, ".//h1"))


def test_fill_registration_form(driver):
    global email, password
    current_time = time.strftime("%H-%M-%S.%d-%b-%Y", time.localtime())

    time.sleep(1)
    first_name = driver.find_element_by_xpath(".//input[@name='firstname']")
    first_name.send_keys("FirstName-" + current_time)

    last_name = driver.find_element_by_xpath(".//input[@name='lastname']")
    last_name.send_keys("LastName-" + current_time)

    address1 = driver.find_element_by_xpath(".//input[@name='address1']")
    address1.send_keys("This is address1: " + current_time)

    postcode = driver.find_element_by_xpath(".//input[@name='postcode']")
    postcode.send_keys(get_random_string_of_numbers(5))

    city = driver.find_element_by_xpath(".//input[@name='city']")
    city.send_keys("This is City: " + current_time)

    email_elem = driver.find_element_by_xpath(".//input[@name='email']")
    email = current_time + "@mail.ru"
    email_elem.send_keys(email)

    phone = driver.find_element_by_xpath(".//input[@name='phone']")
    phone.send_keys("+79" + get_random_string_of_numbers(9))

    country = Select(driver.find_element_by_xpath(".//select[@name='country_code']"))
    country.select_by_visible_text("United States")

    time.sleep(1)
    state = Select(driver.find_element_by_xpath(".//select[@name='zone_code']"))
    index = random.randint(0, len(state.options)-1)
    state.select_by_index(index)

    password_elem = driver.find_element_by_xpath(".//input[@name='password']")
    password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
    password_elem.send_keys(password)

    confirmed_password = driver.find_element_by_xpath(".//input[@name='confirmed_password']")
    confirmed_password.send_keys(password)

    address2 = driver.find_element_by_xpath(".//input[@name='address2']")
    address2.send_keys("This is address2: " + current_time)

    print(email)
    print(password)


def test_click_create_account(driver):
    driver.find_element_by_xpath(".//button[@name='create_account']").click()
    WebDriverWait(driver, 5).until(EC.presence_of_element_located, (By.XPATH, ".//a[text()='Logout']"))


def test_logout(driver):
    driver.find_element_by_xpath(".//a[text()='Logout']").click()
    WebDriverWait(driver, 5).until(EC.presence_of_element_located, (By.XPATH, ".//button[@name='login']"))


def test_login_and_logout(driver):
    driver.find_element_by_xpath(".//input[@name='email']").send_keys(email)
    driver.find_element_by_xpath(".//input[@name='password']").send_keys(password)
    driver.find_element_by_xpath(".//button[@name='login']").click()
    WebDriverWait(driver, 5).until(EC.presence_of_element_located, (By.XPATH, ".//a[text()='Logout']"))

    test_logout(driver)
