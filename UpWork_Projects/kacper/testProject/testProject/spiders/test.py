import scrapy
from scrapy import Selector
from scrapy_selenium import SeleniumRequest
import pandas as pd
import time


class TestSpider(scrapy.Spider):
    name = 'test'
    
    df = pd.read_excel("D:/Web-Scrapping/UpWork_Projects/kacper/testProject/urlsFile.xlsx")

    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.kickstarter.com/discover/advanced?state=successful&category_id=34&woe_id=23424977&sort=newest&seed=2671411&page=5",
            wait_time=10,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        driver.maximize_window()
        for _,value in self.df.iterrows():
            driver.get(value['URL'])
            time.sleep(2)
            html = driver.page_source
            resp_obj = Selector(text=html)
            count = resp_obj.xpath("normalize-space(//b[contains(@class, 'count')]/text())").get()
            yield{
                'Count': count.replace("projects", "").strip()
            }