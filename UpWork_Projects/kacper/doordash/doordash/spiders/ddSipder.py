import scrapy
from scrapy import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


class DdsipderSpider(scrapy.Spider):
    name = 'ddSipder'

    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.doordash.com/food-delivery",
            wait_time=10,
            callback=self.getCityUrls
        )

    def getCityUrls(self, response):
        driver = response.meta['driver']
        driver.maximize_window()

        htmlOtr = driver.page_source
        respObjOtr = Selector(text=htmlOtr)

        for i in range(1,80):            
            stateElem = driver.find_element_by_xpath(f"(//div[contains(@class, 'MarketLinks_markets')]/div/button)[{i}]")
            driver.execute_script("arguments[0].click()", stateElem)
            time.sleep(1)

            htmlInr = driver.page_source
            respObjInr = Selector(text=htmlInr)

            cities = respObjInr.xpath("//div[contains(@class, 'MarketLinks_cities')]/a")
            for city in cities:
                rawUrl = city.xpath(".//@href").get()
                yield scrapy.Request(
                    url=f'''https://api.doordash.com/v2/seo_city_stores/?delivery_city_slug={rawUrl.split("/")[-2]}&store_only=false&limit=50''',
                    method="GET",
                    callback=self.parse,
                    meta={
                        'State': respObjOtr.xpath(f'''normalize-space((//div[contains(@class, 'MarketLinks_markets')]/div/button)[{i}])''').get(),
                        'City': city.xpath("normalize-space(.//text())").get(),
                    }
                )


    def parse(self, response):
        pass
