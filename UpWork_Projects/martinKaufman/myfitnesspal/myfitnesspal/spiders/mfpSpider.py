import scrapy
import time
from scrapy import Selector
from scrapy_selenium import SeleniumRequest
import pandas as pd
from selenium.webdriver.common.keys import Keys


class MfpspiderSpider(scrapy.Spider):
    name = 'mfpSpider'
    
    df = pd.read_excel("D:/Web-Scrapping/UpWork_Projects/martinKaufman/lidl/lidlProducts.xlsx")

    def qty_fix(self, value):
        try:
            li = value[0].split(",")
            word = "".join(i for i in li[-1:])
            return word.strip()
        except:
            return None

    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.myfitnesspal.com/food/search",
            wait_time=5,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        driver.maximize_window()
        for _, value in self.df.iterrows():
            productName = value['Name']
            url = value['product url']
            input_box = driver.find_element_by_xpath("//input[@type='search']")
            input_box.send_keys(f"{productName}, lidl")
            input_box.send_keys(Keys.ENTER)
            time.sleep(3)

            html = driver.page_source
            resp_obj = Selector(text=html)

            calPerQty = self.qty_fix(resp_obj.xpath("(//div[@class='jss49'])[1]/text()").getall())
            calories = resp_obj.xpath("//div[@class='jss54']/text()").get()

            yield {
                'productName': productName,
                'url': url,
                'calPerQty': calPerQty,
                'calories': calories.replace("Calories: ", "")
            }

            driver.find_element_by_xpath("//input[@type='search']").clear()
