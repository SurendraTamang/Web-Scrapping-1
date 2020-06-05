# -*- coding: utf-8 -*-
import scrapy


class WallmartspiderSpider(scrapy.Spider):
    name = 'wallmartSpider'
    allowed_domains = ['www.wallmart.com']
    start_urls = ['http://www.wallmart.com/']

    def parse(self, response):
        pass
