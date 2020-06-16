# -*- coding: utf-8 -*-
import scrapy


class TestspiderSpider(scrapy.Spider):
    name = 'testSpider'
    # allowed_domains = ['www.bestbuy.com']
    # start_urls = ['http://www.bestbuy.com/']

    def start_requests(self):
        yield scrapy.Request(
            url="https://www.bathandbodyworks.com/c/body-care/body-wash-shower-gel",
            callback=self.parse
        )

    def parse(self, response):
        print(response)
