import time
import random

import pytest
from selenium import webdriver

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

t_e = 5


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


def test_click_countries_menu(driver):
    countries = driver.find_element_by_xpath(
        ".//span[text()='Countries']//parent::a")
    time.sleep(1)
    countries.click()
    WebDriverWait(driver, t_e).until(EC.presence_of_element_located(
        (By.XPATH, ".//a[text()=' Add New Country']")))


def test_click_country(driver):
    countries = driver.find_elements_by_xpath(".//tr[@class='row']")
    index = random.randint(0, len(countries) - 1)
    columns = countries[index].find_elements_by_xpath(".//td")
    link = columns[4].find_element_by_xpath("./a")
    link.click()
    WebDriverWait(driver, t_e).until(EC.presence_of_element_located(
        (By.XPATH, ".//h1[text()=' Edit Country']")))


def test_open_external_links(driver):
    external_links = driver.find_elements_by_xpath(
        ".//i[@class='fa fa-external-link']//parent::a")

    # запоминаем id текущего окна
    main_window = driver.current_window_handle

    # запоминаем id всех открытых окон (пока оно одно)
    old_windows = driver.window_handles

    for link in external_links:
        link.click()   # клик для открытия в новом окне

        # ждем появления нового окна
        new_window = WebDriverWait(driver, t_e).until(
            lambda d: list(set(driver.window_handles) - set(old_windows))[0]
            if(len(set(driver.window_handles) - set(old_windows))) else [])

        driver.switch_to.window(new_window)     # переключаемся в новое окно
        driver.close()  # закрываем его
        driver.switch_to.window(main_window)    # переключаемся в исходное окно
