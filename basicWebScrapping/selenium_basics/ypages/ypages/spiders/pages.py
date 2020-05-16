# -*- coding: utf-8 -*-
import scrapy   
from scrapy_selenium import SeleniumRequest


class PagesSpider(scrapy.Spider):
    name = 'pages'

    def start_requests(self):
        search_para = ['beauty', 'health', 'medical']
        for i in search_para:
            yield SeleniumRequest(
                url=f"https://www.yellowpages.com.sg/search/all/{i}",
                wait_time=5,
                callback=self.parse
            )

    def parse(self, response):
        contacts = response.xpath("//h2/a")
        for contact in contacts:
            yield {
                'url': contact.xpath(".//@href").get(),
                'name': contact.xpath(".//text()").get()
            }