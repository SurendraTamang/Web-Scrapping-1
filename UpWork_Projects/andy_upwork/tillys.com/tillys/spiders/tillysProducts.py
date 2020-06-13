# -*- coding: utf-8 -*-
import scrapy
import pandas as pd


class TillysproductsSpider(scrapy.Spider):
    name = 'tillysProducts'
    
    df = pd.read_excel("D:/sipun/Web-Scrapping/UpWork_Projects/andy_upwork/tillys.com/subCatURLS.xlsx")

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

        listings = response.xpath("//li[contains(@class, 'grid-tile')]")
        for lists in listings:
            yield {
                'name': lists.xpath("normalize-space(.//div[@class='product-name']/a/text())").get(),
                'price': lists.xpath("normalize-space(.//span[contains(@title, 'Price')][last()])").get(),
                'category': category,
                'sub_category': sub_category,
                'url': lists.xpath(".//div[@class='product-name']/a/@href").get()
            }

        next_page = response.xpath("//a[@title='Go to next page']/@href").get()
        if next_page:
            yield scrapy.Request(
                url=next_page,
                callback=self.parse,
                meta={
                    'category': category,
                    'sub_category': sub_category
                }
            )
