# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from scrapy_selenium import SeleniumRequest


class FbspiderSpider(scrapy.Spider):
    name = 'fbSpider'
    urls_list = [
        'https://www.fivebelow.com/pet.html',
        'https://www.fivebelow.com/books.html',
        'https://www.fivebelow.com/sports.html',
        'https://www.fivebelow.com/create.html',
        'https://www.fivebelow.com/party.html',
        'https://www.fivebelow.com/candy.html',
        'https://www.fivebelow.com/style.html',
        'https://www.fivebelow.com/beauty.html',
        'https://www.fivebelow.com/play.html',
        'https://www.fivebelow.com/tech.html',
        'https://www.fivebelow.com/room.html',
        'https://www.fivebelow.com/fitness-wellness.html',
        'https://www.fivebelow.com/home-essentials.html',
        'https://www.fivebelow.com/summer.html'
    ]
    cat_list = ['pet', 'books', 'sports', 'create', 'party', 'candy', 'style', 'beauty', 'play', 'tech', 'room', 'fitness-wellness', 'home-essentials', 'summer']    

    def start_requests(self):
        for cat_url, cat in zip(self.urls_list, self.cat_list):
            yield scrapy.Request(
                url=cat_url,
                callback=self.sub_cat_listings,
                meta={
                    'category': cat
                }
            )

    def sub_cat_listings(self, response):
        category = response.request.meta['category']
        listings = response.xpath("//figcaption[@data-element='caption']/parent::figure")
        for lists in listings:
            yield scrapy.Request(
                url=lists.xpath("normalize-space(.//a/@href)").get(),
                callback=self.parse,
                meta={
                    'sub-category': lists.xpath("normalize-space(.//figcaption/text())").get(),
                    'category': category
                }
            )

    def parse(self, response):
        sub_category = response.request.meta['sub-category']
        category = response.request.meta['category']
        #category = response.xpath("normalize-space(//div[@class='breadcrumbs']/ul/li[2]/a/text())").get()
        listings = response.xpath("//li[contains(@class,'product-item')]")
        for lists in listings:
            yield{
                'product_name': lists.xpath("normalize-space(.//a[@class='product-item-link']/text())").get(),
                'product_category': category,
                'product_sub_category': sub_category,
                'product_price': lists.xpath("normalize-space(.//span[@class='price']/text())").get(),
                'product_url': lists.xpath("normalize-space(.//a[@class='product-item-link']/@href)").get()
            }

        next_page = response.xpath("(//a[@class='action  next']/@href)[2]").get()
        if next_page:
            yield scrapy.Request(
                url=next_page,
                callback=self.parse,
                meta={
                    'sub-category': sub_category,
                    'category': category
                }
            )
