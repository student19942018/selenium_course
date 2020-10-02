from selenium import webdriver
from pages.main_page import MainPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage

from functools import reduce


class Application:

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        self.driver = webdriver.Chrome(options=options)

        self.main_page = MainPage(self.driver)
        self.product_page = ProductPage(self.driver)
        self.cart_page = CartPage(self.driver)
        self.products = {}

    def quit(self):
        self.driver.quit()

    def add_product(self, new_product):
        count = self.products.get(new_product, 0)  # вернёт 0, если ключа нет
        if count:
            self.products[new_product] += 1
        else:
            self.products[new_product] = 1

    def delete_product(self, name_product):
        self.products.pop(name_product)
        print(self.products)

    def check_count_products(self, count_products):
        # initial=0 для обработки пустого списка
        return reduce(lambda x, y: x + y, self.products.values(), 0) == \
               count_products

    def fill_cart(self, count_products=3):
        for _ in range(count_products):
            name = self.main_page.open().click_product()
            self.add_product(name)
            self.product_page.add_to_cart()

        self.check_count_products(count_products)

    def clear_cart(self):
        self.cart_page.open()
        while len(self.products) > 0:
            name = self.cart_page.delete_product(self.products)
            self.delete_product(name)

        self.cart_page.check_empty_cart()
        self.check_count_products(0)
