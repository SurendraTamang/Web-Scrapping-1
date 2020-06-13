# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy import Selector


class WomenurlSpider(scrapy.Spider):
    name = 'womenUrl'
    # allowed_domains = ['zumiez.com']
    # start_urls = ['http://zumiez.com/']

    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.zumiez.com/snow",
            wait_time=5,
            callback=self.parse
        )

    def parse(self, response):
        pass
        # driver = response.meta['driver']

        # html = driver.page_source
        # selector_obj = Selector(text=html)

        # listings = selector_obj.xpath("//li[@class='accordion-item']")
        # for lists in listings:
        #     category = lists.xpath("normalize-space(.//a/text())").get()
        #     sub_cat_listings = lists.xpath(".//ul/li")
        #     for sclists in sub_cat_listings:
        #         sub_category = sclists.xpath("normalize-space(.//a/text())").get()
        #         url = sclists.xpath(".//a/@href").get()
        #         yield{
        #             'category': category,
        #             'sub_category': sub_category,
        #             'url': url
        #         }
    
    
    
    # Link Extractor For women Category

    # def parse(self, response):
    #     driver = response.meta['driver']

    #     html = driver.page_source
    #     selector_obj = Selector(text=html)

    #     listings = selector_obj.xpath("//ul[@id='womens-nav']/li[@role='menuitem']")
    #     for lists in listings:
    #         category = f'''Women's {lists.xpath("normalize-space(.//a/text())").get()}'''
    #         sub_cat_listings = lists.xpath(".//ul/li")
    #         for sclists in sub_cat_listings:
    #             sub_category = sclists.xpath("normalize-space(.//a/text())").get()
    #             url = sclists.xpath(".//a/@href").get()
    #             yield{
    #                 'category': category,
    #                 'sub_category': sub_category,
    #                 'url': url
    #             }

