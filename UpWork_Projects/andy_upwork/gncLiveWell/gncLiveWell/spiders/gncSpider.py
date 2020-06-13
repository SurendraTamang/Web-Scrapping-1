# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy import Selector
import time


class GncspiderSpider(scrapy.Spider):
    name = 'gncSpider'
    cntr = 1
    
    def start_requests(self):
        yield SeleniumRequest(
            url='https://www.google.com',
            wait_time=10,
            callback = self.subCat_url
        )

    # def cat_url(self, response):
    #     driver = response.meta['driver']
    #     time.sleep(6)
    #     html = driver.page_source
    #     response_obj = Selector(text=html)
    #     cat_listings = response_obj.xpath("//a[@href='https://www.gnc.com/department/']/following-sibling::div/div/ul")
    #     for c_url in cat_listings[2]:
    #         yield scrapy.Request(
    #             url=c_url.xpath("normalize-space(.//a/@href)").get(),
    #             callback=self.subCat_url,
    #             meta={
    #                 'category': c_url.xpath("normalize-space(.//a/text())").get()
    #             }
    #         )
    
    def subCat_url(self, response):
        # driver = response.meta['driver']
        # driver.get("https://www.gnc.com/equipment-accessories")
        # time.sleep(10)
        # html = driver.page_source
        # response_obj = Selector(text=html)
        # subCat_listings = response_obj.xpath("//ul[@id='category-level-1']/li[@class='expandable active']/ul/li[@class='expandable']")
        # for sc_url in subCat_listings:
        yield scrapy.Request(
            #url=sc_url.xpath("normalize-space(.//a/@href)").get(),
            url="https://www.gnc.com/beauty-skin-care/hair-care/",
            callback=self.parse,
            meta={
                'category': "Beauty & Skin Care",
                # 'sub_category': sc_url.xpath("normalize-space(.//a/text())").get(),
                'sub_category': "Hair Care"
            }
        )

    def parse(self, response):
        category = response.request.meta['category']
        sub_category = response.request.meta['sub_category']
        prod_listings = response.xpath("//ul[@id='search-result-items']/li")
        for products in prod_listings:
            yield {
                'productName': products.xpath("normalize-space(.//div[@class='product-name']/a/text())").get(),
                'price': products.xpath("normalize-space(.//div[@class='product-pricing']/span/text())").get(),
                'category': category,
                'sub_category': sub_category,
                'productURL': products.xpath("normalize-space(.//div[@class='product-name']/a/@href)").get()
            }

        self.cntr += 1
        if response.xpath(f"//a[text()={self.cntr}]"):
            yield scrapy.Request(
                url=response.xpath(f"//a[text()={self.cntr}]/@href").get(),
                callback=self.parse,
                meta={
                    'category': category,
                    'sub_category': sub_category
                }
            )
        else:
            self.cntr = 1
