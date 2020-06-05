# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy import Selector


class CapterraspiderSpider(scrapy.Spider):
    name = 'capterraSpider'
    allowed_domains = ['capterra.com']
    start_urls = ['http://capterra.com/']

    def start_requests(self):
        yield scrapy.Request(
            url="https://www.capterra.com/categories",
            callback = self.cat_listings
        )

    def cat_listings(self, response):
        category_urls = response.xpath("//div[@class='cell  one-whole']")
        for url in category_urls:
            cat_url = f'https://www.capterra.com{url.xpath(".//li/a/@href").get()}'
            yield SeleniumRequest(
                url=cat_url,
                wait_time=6,
                callback=self.cat_url
            )

    def cat_url(self, response):
        driver = response.meta['driver']
        while True:
            html = driver.page_source
            response_obj = Selector(text=html)
            if response_obj.xpath("//div[text()='Show More']"):
                driver.find_element_by_xpath("//div[text()='Show More']").click()
            else:
                break
        html = driver.page_source
        response_obj = Selector(text=html)
        listings = response_obj.xpath("//div[contains(@class, 'eiRAVe')]")
        for listing in listings:
            listing_url = f'https://www.capterra.com{listing.xpath(".//h2/a/@href").get()}'
            yield scrapy.Request(
                url=listing_url,
                callback=self.parse
            )

    def parse(self, response):
        yield{
            'name': response.xpath("//div[contains(@class, 'eiuUqb')]/h1/text()").get(),
            'category': response.xpath("(//div[@class='Crumb__CrumbText-sc-1luy9u1-2 gmyPIG']/text())[2]").get(),
            'no_of_reviews': response.xpath("//div[@class='StarRating__Count-sc-9jwzgg-2 iQfOTw']/text()").get(),
            'rating': response.xpath("//div[@class='StarRating__Rating-sc-9jwzgg-1 cAGyvf']/text()").get(),
            'url': response.xpath("(//p[@class='ProductSummary__CompanyDetailItem-uex5jn-5 fxpGcm']/text())[2]").get()
        }