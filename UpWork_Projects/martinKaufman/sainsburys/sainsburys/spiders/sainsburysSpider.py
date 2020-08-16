import scrapy
import time
from scrapy import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class SainsburysspiderSpider(scrapy.Spider):
    name = 'sainsburysSpider'
    
    categoryURLs = [
        'https://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/seeall?fromMegaNav=1',
        'https://www.sainsburys.co.uk/shop/gb/groceries/dietary-and-lifestyle/seeall?fromMegaNav=1',
        'https://www.sainsburys.co.uk/shop/gb/groceries/meat-fish/seeall?fromMegaNav=1',
        'https://www.sainsburys.co.uk/shop/gb/groceries/dairy-eggs-and-chilled/seeall?fromMegaNav=1',
        'https://www.sainsburys.co.uk/shop/gb/groceries/bakery/seeall?fromMegaNav=1',
        'https://www.sainsburys.co.uk/shop/gb/groceries/frozen-/seeall?fromMegaNav=1',
        'https://www.sainsburys.co.uk/shop/gb/groceries/food-cupboard/seeall?fromMegaNav=1',
        'https://www.sainsburys.co.uk/shop/gb/groceries/drinks/seeall?fromMegaNav=1'
    ]

    def getQuantity(self, value):
        try:
            li = value.slpit(" ")
            result = li[-1:]
            if bool(re.search(r'\d', result)):
                return result
            else:
                result="".join(i for i in li[-2:])
                if bool(re.search(r'\d', result)):
                    return result
                else:
                    return None
        except:
            return None

    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.sainsburys.co.uk",
            wait_time=5,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        driver.maximize_window()
        for categoryURL in self.categoryURLs:
            driver.get(categoryURL)
            while True:
                WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//li[@class='gridItem']")))
                time.sleep(3)
                html1 = driver.page_source
                response1 = Selector(text=html1)
                
                products = response1.xpath("//li[@class='gridItem']")

                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[1])
                
                for product in products:
                    driver.get(product.xpath(".//h3/a/@href").get())
                    try:
                        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//img[contains(@class, 'pd__image')]")))
                    except:
                        pass
                    time.sleep(1)
                    html2 = driver.page_source
                    response2 = Selector(text=html2)
                    name = response2.xpath("normalize-space(//h1/text())").get()
                    sSize = response2.xpath("normalize-space(//tr[@class='tableTitleRow']/th[2]/text())").get()
                    if sSize  == "":
                        sSize = response2.xpath("normalize-space(//tr/th[2]/text())").get()
                    calories = response2.xpath("normalize-space(//tbody/tr[2]/td/text())").get()
                    if "kcal" not in calories:
                        calories = response2.xpath("normalize-space(//tbody/tr/td/text())").get()
                    yield {
                        'Name of Food Item': name,
                        'Serving Size of Food Item': sSize,
                        'Price': response2.xpath("normalize-space(//div[@data-test-id='pd-retail-price']/text())").get(),
                        'Number of Calories Per Serving': calories,
                        'Image (link)': response2.xpath("//img[contains(@class, 'pd__image')]/@src").get(),
                        'Product (link)': driver.current_url,
                        'Lvl1 Category': response2.xpath("normalize-space(//ol/li[1]/a/text())").get(),
                        'Lvl2 Category': response2.xpath("normalize-space(//ol/li[2]/a/text())").get(),
                        'quantity': self.getQuantity(name)
                    }

                driver.close()  
                driver.switch_to.window(driver.window_handles[0])

                nextPage = response1.xpath("//li[@class='next']/a/@href").get()
                if nextPage:
                    driver.get(nextPage)
                else:
                    break

