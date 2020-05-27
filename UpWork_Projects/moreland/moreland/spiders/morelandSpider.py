# -*- coding: utf-8 -*-
import scrapy


class MorelandspiderSpider(scrapy.Spider):
    name = 'morelandSpider'
    allowed_domains = ['moreland.com']
    start_urls = ['http://moreland.com/']

    def parse(self, response):
        pass
