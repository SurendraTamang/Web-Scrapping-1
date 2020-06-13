# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy import Selector
import pandas as pd
import time


class LinkextractSpider(scrapy.Spider):
    name = 'linkExtract'

    df = pd.read_excel("D:/sipun/Web-Scrapping/UpWork_Projects/andy_upwork/tillys.com/urls.xlsx")
    
    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.google.com",
            wait_time=3,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        driver.maximize_window()
        for _, value in self.df.iterrows():
            driver.get(value['url'])
            time.sleep(5)

            html = driver.page_source
            response_obj = Selector(text=html)

            listings = response_obj.xpath("(//div[contains(@class, 'category-refinement')])[2]/ul/li")
            for lists in listings:
                yield{
                    'url': lists.xpath(".//a/@href").get(),
                    'category': value['category'],
                    'sub_category': lists.xpath("normalize-space(.//a/text())").get()
                }
