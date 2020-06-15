# -*- coding: utf-8 -*-
import scrapy
import pandas as pd


class BbprodsSpider(scrapy.Spider):
    name = 'bbProds'
    # allowed_domains = ['www.bestbuy.com']
    # start_urls = ['http://www.bestbuy.com/']

    df = pd.read_excel("C:/Users/byom/Desktop/best buy urls.xlsx")

    def start_requests(self):
        for _, value in self.df.iterrows():
            yield scrapy.Request(
                url=value['url'],
                callback=self.parse,
                meta={
                    'lvl1_cat': value['lvl1_cat'],
                    'lvl2_cat': value['lvl2_cat'],
                    'lvl3_cat': value['lvl3_cat']
                }
            )

    def parse(self, response):
        lvl1_cat = response.request.meta['lvl1_cat']
        lvl2_cat = response.request.meta['lvl2_cat']
        lvl3_cat = response.request.meta['lvl3_cat']
        prod_listings = response.xpath("//ol[@class='sku-item-list']/li")
        for prod in prod_listings:
            yield {
                'product_name': prod.xpath("normalize-space(.//h4/a/text())").get(),
                'price': prod.xpath("normalize-space(.//div[contains(@class, 'priceView-customer-price')]/span[1]/text())").get(),
                'lvl1_cat': lvl1_cat,
                'lvl2_cat': lvl2_cat,
                'lvl3_cat': lvl3_cat,                
                'url': f'''https://www.bestbuy.com{prod.xpath(".//h4/a/@href").get()}'''
            }

        next_page = response.xpath("//a[@class='sku-list-page-next']/@href").get()
        if next_page:
            yield scrapy.Request(
                url=next_page,
                callback=self.parse,
                meta={
                    'lvl1_cat': lvl1_cat,
                    'lvl2_cat': lvl2_cat,
                    'lvl3_cat': lvl3_cat
                }
            )
