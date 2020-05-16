# -*- coding: utf-8 -*-
import scrapy


class KeysSpider(scrapy.Spider):
    name = 'keys'
    #allowed_domains = ['keys.lol/ethereum/1']
    #start_urls = ['http://keys.lol/ethereum/5/']

    def start_requests(self):
        yield scrapy.Request(
            url='http://keys.lol/ethereum/5/',
            meta = {
                    'dont_redirect': True,
                    'handle_httpstatus_list': [302]
                  },
            callback=self.parse
        )

    def parse(self, response):
        keys = response.xpath("//div[contains(@class, 'wallet')]")
        for key in keys:
            formula = key.xpath("normalize-space(.//span/a/text())").get()
            yield {
                "Formula": formula
            }
           
        next_page = response.xpath("//a[contains(@title, 'Next page')]/@href").get()
        if next_page:
            yield response.follow(
                url=next_page,
                meta = {
                    'dont_redirect': True,
                    'handle_httpstatus_list': [302]
                  },
                callback=self.parse
                )