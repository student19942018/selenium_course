
def is_element_present(driver, locator):
    return len(driver.find_elements_by_xpath(locator)) > 0
