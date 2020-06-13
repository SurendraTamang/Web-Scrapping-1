# -*- coding: utf-8 -*-
import scrapy
import pandas as pd


class ZumiezproductsSpider(scrapy.Spider):
    name = 'zumiezProducts'

    df = pd.read_excel("D:/sipun/Web-Scrapping/UpWork_Projects/andy_upwork/zumiez/cat_url.xlsx")

    def start_requests(self):
        for _, value in self.df.iterrows():
            yield scrapy.Request(
                url=value['url'],
                callback=self.parse,
                meta={
                    'category': value['category'],
                    'sub_category': value['sub_category']
                }
            )
    
    def parse(self, response):
        category = response.request.meta['category']
        sub_category = response.request.meta['sub_category']
        products = response.xpath("//div[@class='item']")
        for product in products:
            yield{
                'product_name': product.xpath("normalize-space(.//h2/a/text())").get(),
                'price': product.xpath("normalize-space(.//span[@class='price']/text())").get(),
                'category': category,
                'sub_category': sub_category,
                'url': product.xpath("normalize-space(.//h2/a/@href)").get()
            }

        next_page = response.xpath("//a[@title='Next']/@href").get()
        if next_page:
            yield scrapy.Request(
                url=next_page,
                callback=self.parse,
                meta={
                    'category': category,
                    'sub_category': sub_category
                }                
            )
