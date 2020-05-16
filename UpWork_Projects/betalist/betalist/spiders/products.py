# -*- coding: utf-8 -*-
import scrapy


class ProductsSpider(scrapy.Spider):
    name = 'products'

    def start_requests(self):
        yield scrapy.Request(
            url="https://betalist.com/markets",
            callback=self.category_page
        )

    def category_page(self, response):
        categories = response.xpath("//ul[@class='markets']/li")
        for category in categories[300:]:
            abs_url = f'''https://betalist.com{category.xpath(".//a/@href").get()}'''
            cat_name = category.xpath("normalize-space(.//a/text()[1])").get()
            yield scrapy.Request(
                url=abs_url,
                callback=self.product_page,
                meta={
                    'category': cat_name
                }
            )

    def product_page(self, response): 
        listings = response.xpath("//div[@class='startupDeck']/div/a")
        for listing in listings:
            abs_url = f'''https://betalist.com{listing.xpath(".//@href").get()}'''
            yield scrapy.Request(
                url=abs_url,
                callback=self.parse,
                meta={
                    'category': response.request.meta['category'],
                    'url': response.url
                }
            )
        cat_name = response.request.meta['category']
        next_page = response.xpath("//a[text()='More']/@href").get()
        if next_page:
            abs_url = f"https://betalist.com{next_page}"
            yield scrapy.Request(
                url=abs_url,
                callback=self.product_page,
                meta={
                    'category': cat_name
                }
            )

    def parse(self, response):
        yield {
            'product_name': response.xpath("(//h1[contains(@class, 'startup__summary__name')])[2]/text()").get(),
            'description': response.xpath("(//h2[contains(@class, 'startup__summary__pitch')])[2]/text()").get(),
            'website_url': f'''https://betalist.com{response.xpath("//div[contains(@class, 'social button2bar')]/a/@href").get()}''',
            'tags': response.request.meta['category'],
            'votes': response.xpath("//div[@class='social button2bar']//div[@class='cuteButton__score']/text()").get(),
            'page_source_url': response.request.meta['url']
        }
        
