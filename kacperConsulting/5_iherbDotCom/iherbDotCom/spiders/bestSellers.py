# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class BestsellersSpider(scrapy.Spider):
    name = 'bestSellers'

    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.iherb.com",
            wait_time=5,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        driver.maximize_window()
        driver.get('https://www.iherb.com/catalog/topsellers')
        input()
        time.sleep(5)

        html = driver.page_source
        respObj = Selector(text=html)

        tsProds = respObj.xpath("//div[contains(@class, 'top-sellers-row')][last()]/div")
        for tsProd in tsProds:
            category = tsProd.xpath("normalize-space(.//h3/text())").get()
            prods = tsProd.xpath(".//div[@class='description']/a/@href").getall()
            for prod in prods:
                yield{
                    'Category': category,
                    'url': prod
                }
