# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from scrapy_selenium import SeleniumRequest
import time


class CatlinkextractSpider(scrapy.Spider):
    name = 'catLinkExtract'

    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.familydollar.com/cleaning/laundry-care-fd",
            wait_time=3,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        driver.maximize_window()
        time.sleep(20)

        html = driver.page_source
        response_obj = Selector(text=html)

        listings = response_obj.xpath("//div[@class='submenu-container']")
        for lists in listings:
            category = lists.xpath("normalize-space(.//span/text())").get()
            sub_listings = lists.xpath(".//div[@class='shop-bd-items']/li")
            for sub_lists in sub_listings:
                yield{
                    'category': category,
                    'sub_category': sub_lists.xpath("normalize-space(.//a/text())").get(),
                    'sub_category_url': f'https://www.familydollar.com{sub_lists.xpath("normalize-space(.//a/@href)").get()}'      
                }
