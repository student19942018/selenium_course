import time

from selenium.webdriver.support.ui import Select

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from helpers.helpers import is_element_present


class ProductPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def add_to_cart(self):
        locator_counter = ".//span[@class='quantity']"
        count_items = int(self.driver.
                          find_element_by_xpath(locator_counter).text)

        if is_element_present(self.driver, ".//select[@name='options[Size]']"):
            select = Select(
                self.driver.find_element_by_xpath(
                    ".//select[@name='options[Size]']"))
            select.select_by_index(1)   # выбираем первый имеющийся размер

        time.sleep(1)
        self.driver.find_element_by_xpath(
            ".//button[@name='add_cart_product']").click()

        self.wait.until(
            EC.text_to_be_present_in_element(
                (By.XPATH, locator_counter), str(count_items + 1)))
