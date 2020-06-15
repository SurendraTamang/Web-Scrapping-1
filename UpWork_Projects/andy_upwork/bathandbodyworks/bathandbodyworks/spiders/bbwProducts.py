# -*- coding: utf-8 -*-
import scrapy
import pandas as pd


class BbwproductsSpider(scrapy.Spider):
    name = 'bbwProducts'

    df = pd.read_excel("D:/Web-Scrapping/UpWork_Projects/andy_upwork/bathandbodyworks/bath & bodyworks.xlsx")
    
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

        listings = response.xpath("//ul[@id='search-result-items']/li")
        for prods in listings:
            yield {
                'product_name': f'''{prods.xpath("normalize-space(.//div[@class='product-name']/text())").get()} {prods.xpath("normalize-space(.//div[@class='product-type']/text())").get()}''',
                'price': prods.xpath(".//div[@class='product-pricing']/span/text()").get(),
                'lvl1_cat': lvl1_cat,
                'lvl2_cat': lvl2_cat,
                'lvl3_cat': lvl3_cat,
                'url': f'''https://www.bathandbodyworks.com{prods.xpath(".//a/@href").get()}'''
            }

        next_page = response.xpath("//a[@title='Go to next page']/@href").get()
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
