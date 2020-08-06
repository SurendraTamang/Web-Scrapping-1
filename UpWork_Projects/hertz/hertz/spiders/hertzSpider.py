# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from scrapy_selenium import SeleniumRequest
import time


class HertzspiderSpider(scrapy.Spider):
    name = 'hertzSpider'
    
    def start_requets(self):
        yield SeleniumRequest(
            url="https://www.hertz.com/rentacar/location#cities",
            wait_time=6,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        driver.sleep(5)

        for i in range(1,157):
            driver.find_element_by_xpath(f"(//ul[@class='coln-list']/li/a)[{i}]").click()
            
            

            # To go back
            driver.find_element_by_xpath("//span[text()='Full Location List']/following-sibling::a").click()
