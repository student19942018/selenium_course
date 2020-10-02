from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class MainPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get("http://localhost/litecart/en/")
        self.wait.until(EC.title_is("Online Store | My Store"))
        return self

    def click_product(self):
        first_product = self.driver.find_elements_by_xpath(
            ".//li[contains(@class, 'product')]")[0]
        name = first_product.find_element_by_xpath(
            ".//div[@class='name']").text
        first_product.find_element_by_xpath(".//a[@class='link']").click()
        h1 = self.wait.until(
            EC.presence_of_element_located((By.XPATH, ".//h1")))
        assert h1.text == name
        return name
