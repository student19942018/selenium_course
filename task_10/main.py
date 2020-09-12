import pytest
from selenium import webdriver

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from msedge.selenium_tools import Edge, EdgeOptions


browser = "IE"
product_on_main = {}
product_on_page = {}


def get_rgb(string):
    # переводит rgba/rgb-строку в целочисленный rgb-список
    # return [int(x) for x in string[5:-4].split(", ")]  # только для rgba
    # return [int(x) for x in string[4:-1].split(", ")]  # только для rgb

    # для rgba/rgb
    return [int(x) for x in string.split("(")[1].split(")")[0].split(", ")][:3]


def check_matching_colors(a, b, price):
    # цвета на разных страницах могут не совпадать
    if a == b:
        print("Цвет {} цены совпадает на страницах".format(price))
    else:
        print("Цвет {} цены НЕ совпадает на страницах".format(price))


@pytest.fixture(scope="session")
def driver(request):
    if browser == "Chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        wd = webdriver.Chrome(options=options)

    if browser == "Firefox":
        wd = webdriver.Firefox(firefox_binary="C:\\Program Files\\Mozilla Firefox\\firefox.exe")

    if browser == "Firefox ESR":
        wd = webdriver.Firefox(capabilities={"marionette": False},
                               firefox_binary="C:\\Program Files\\Mozilla Firefox ESR\\firefox.exe")

    if browser == "Firefox Nightly":
        wd = webdriver.Firefox(firefox_binary="C:\\Program Files\\Firefox Nightly\\firefox.exe")

    if browser == "Microsoft Edge":
    # Microsoft Edge (based on Chromium)
    # https://github.com/microsoft/edge-selenium-tools
    # https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
        options = EdgeOptions()
        options.use_chromium = True
        wd = Edge(options=options, capabilities={"unexpectedAlertBehaviour": "dismiss"})
        print(wd.capabilities)

    if browser == "IE":
        wd = webdriver.Ie(capabilities={"requireWindowFocus": True})

    request.addfinalizer(wd.quit)
    return wd


def test_open_product_page(driver):
    global product_on_main, product_on_page

    driver.get("http://localhost/litecart/en/")
    product = driver.find_element_by_xpath(".//div[@id='box-campaigns']")
    regular_price = product.find_element_by_xpath(".//s[@class='regular-price']")
    campaign_price = product.find_element_by_xpath(".//strong[@class='campaign-price']")

    product_on_main["name"] = product.find_element_by_xpath(".//div[@class='name']").text
    product_on_main["regular_price_value"] = regular_price.text
    product_on_main["regular_price_color"] = regular_price.value_of_css_property("color")
    product_on_main["regular_price_font_size"] = regular_price.value_of_css_property("font-size")
    product_on_main["campaign_price_value"] = campaign_price.text
    product_on_main["campaign_price_color"] = campaign_price.value_of_css_property("color")
    product_on_main["campaign_price_font_size"] = campaign_price.value_of_css_property("font-size")
    product_on_main["campaign_price_font-weight"] = campaign_price.value_of_css_property("font-weight")
    print()
    print(product_on_main)

    driver.execute_script("arguments[0].scrollIntoView(true);", product)
    product.find_element_by_xpath(".//div[contains(@class, 'sticker')]").click()
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, ".//h1")))

    product = driver.find_element_by_xpath(".//div[@id='box-product']")
    regular_price = product.find_element_by_xpath(".//s[@class='regular-price']")
    campaign_price = product.find_element_by_xpath(".//strong[@class='campaign-price']")

    product_on_page["name"] = product.find_element_by_xpath(".//h1[@class='title']").text
    product_on_page["regular_price_value"] = regular_price.text
    product_on_page["regular_price_color"] = regular_price.value_of_css_property("color")
    product_on_page["regular_price_font_size"] = regular_price.value_of_css_property("font-size")
    product_on_page["campaign_price_value"] = campaign_price.text
    product_on_page["campaign_price_color"] = campaign_price.value_of_css_property("color")
    product_on_page["campaign_price_font_size"] = campaign_price.value_of_css_property("font-size")
    product_on_page["campaign_price_font-weight"] = campaign_price.value_of_css_property("font-weight")
    print(product_on_page)


def test_check_name_product(driver):
    # а) на главной странице и на странице товара совпадает текст названия товара
    assert product_on_main["name"] == product_on_page["name"]


def test_check_prices_product(driver):
    # б) на главной странице и на странице товара совпадают цены (обычная и акционная)
    assert product_on_main["regular_price_value"] == product_on_page["regular_price_value"]
    assert product_on_main["campaign_price_value"] == product_on_page["campaign_price_value"]


def test_check_color_regular_price(driver):
    # в) обычная цена - зачёркнутая и серая, проверка на каждой странице
    # зачеркнутость проверена, т.к. был поиск по тегу <s>
    print()
    rgb_on_main = get_rgb(product_on_main["regular_price_color"])
    print(rgb_on_main)
    assert rgb_on_main[0] == rgb_on_main[1] and rgb_on_main[1] == rgb_on_main[2]

    rgb_on_page = get_rgb(product_on_page["regular_price_color"])
    print(rgb_on_page)
    assert rgb_on_page[0] == rgb_on_page[1] and rgb_on_page[1] == rgb_on_page[2]

    # совпадает ли цвет на разных страницах ?
    check_matching_colors(rgb_on_main, rgb_on_page, "regular")


def test_check_style_campaign_price(driver):
    # г) акционная жирная и красная, проверка на каждой странице
    print()
    rgb_on_main = get_rgb(product_on_main["campaign_price_color"])
    print(rgb_on_main)
    assert rgb_on_main[1] == 0 and rgb_on_main[2] == 0

    rgb_on_page = get_rgb(product_on_page["campaign_price_color"])
    print(rgb_on_page)
    assert rgb_on_page[1] == 0 and rgb_on_page[2] == 0

    # жирный текст - тот, у которого font-weight >= 700 (к тому же у элемента есть тег <strong> )
    # https://www.w3.org/TR/css-fonts-3/#font-weight-numeric-values
    assert int(product_on_main["campaign_price_font-weight"]) >= 700
    assert int(product_on_page["campaign_price_font-weight"]) >= 700

    # совпадает ли цвет на разных страницах ?
    check_matching_colors(rgb_on_main, rgb_on_page, "campaign")


def test_check_campaign_larger_regular_price(driver):
    # д) акционная цена крупнее, чем обычная. проверка на каждой странице
    assert float(product_on_main["campaign_price_font_size"][:-2]) > \
           float(product_on_main["regular_price_font_size"][:-2])

    assert float(product_on_page["campaign_price_font_size"][:-2]) > \
           float(product_on_page["regular_price_font_size"][:-2])
