from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time

from helpers.helpers import is_element_present


class CartPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        time.sleep(1)
        self.driver.get("http://localhost/litecart/en/checkout")
        self.wait.until(EC.title_is("Checkout | My Store"))

    def check_empty_cart(self):
        self.wait.until(
            EC.text_to_be_present_in_element(
                (By.XPATH, ".//em"), "There are no items in your cart."))

    def delete_product(self, products_in_cart):
        rows = self.driver.find_elements_by_xpath(
            ".//table[@class='dataTable rounded-corners']//td[@class='item']//parent::tr")
        assert len(rows) == len(products_in_cart)
        print("\n Кол-во строк в таблице и элементов в products совпадает = {}".format(len(rows)))

        if is_element_present(self.driver, ".//li[@class='shortcut']"):
            shortcuts = self.driver.find_elements_by_xpath(
                ".//li[@class='shortcut']")
            print("Число карточек в Превью = {}".format(len(shortcuts)))
            shortcuts[0].find_element_by_xpath(".//a").click()

        viewport_product = self.driver.find_element_by_xpath(".//li[@class='item']")
        name_product = viewport_product.find_element_by_xpath(".//strong").text
        quantity_product = int(rows[0].find_elements_by_xpath(".//td")[0].text)
        assert products_in_cart[name_product] == quantity_product

        print(products_in_cart)
        print(name_product)

        delete_button = viewport_product.find_element_by_xpath(".//button[@name='remove_cart_item']")
        time.sleep(1)
        delete_button.click()
        self.wait.until(EC.staleness_of(rows[0]))

        return name_product
