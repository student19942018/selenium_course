import time

import pytest
from selenium import webdriver

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium.webdriver.common.action_chains import ActionChains


@pytest.fixture(scope="session")
def driver(request):
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    wd = webdriver.Chrome(chrome_options=options)
    request.addfinalizer(wd.quit)
    return wd


def test_login(driver):
    driver.get("http://localhost/litecart/admin/")
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()


def test_click_items_menu(driver):
    wait = WebDriverWait(driver, 10)  # seconds
    items = driver.find_elements_by_xpath(".//li[@id='app-']")
    count_items = len(items)
    print(count_items)
    item = items[0]
    for i in range(count_items):
        print(str(i + 1) + " - " + item.text)
        time.sleep(1)
        item.click()
        head_item = wait.until(EC.presence_of_element_located((By.XPATH, ".//h1")))
        print(head_item.text)

        subitems = driver.find_elements_by_xpath(".//li[@id='app-' and @class='selected']//li")
        count_subitems = len(subitems)
        if count_subitems:
            for _ in range(1, count_subitems):
                subitem = driver.find_element_by_xpath(".//ul[@class='docs']//li[@class='selected']/following-sibling::li")

                actions = ActionChains(driver)
                actions.move_to_element(subitem)
                actions.perform()

                time.sleep(1)
                subitem.click()
                head_subitem = wait.until(EC.presence_of_element_located((By.XPATH, ".//h1")))
                print(head_subitem.text)

        if (i + 1 != count_items):
            item = driver.find_element_by_xpath(".//li[@id='app-' and @class='selected']/following-sibling::li")
