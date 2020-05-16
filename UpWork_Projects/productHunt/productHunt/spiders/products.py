# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
import pandas as pd
import time


class ProductsSpider(scrapy.Spider):
    name = 'products'

    df = pd.read_excel("D:/upworkWorkspace/Testing/productHunt/category_url.xlsx", sheet_name='set2')

    def scroll(self, driver, timeout):
        scroll_pause_time = timeout
        cntr = 0

        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        while cntr != 500:
            print(cntr)
            cntr += 1
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(scroll_pause_time)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                # If heights are the same it will exit the function
                break
            last_height = new_height

    def start_requests(self):        
        yield SeleniumRequest(
            url='https://www.producthunt.com',
            wait_time=5,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']

        for _, value in self.df.iterrows():
            url = value['cat_urls']
            driver.get(url)
            time.sleep(3)
            self.scroll(driver, 4)
            time.sleep(2)
            # for _ in range(50):
            #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            #     time.sleep(3)

            html = driver.page_source
            response_obj = Selector(text=html)

            listings = response_obj.xpath("//ul[@class='postsList_b2208']/li")
            for listing in listings:
                yield{
                    'product_name' : listing.xpath(".//div[@class='content_31491']/h3/text()").get(),
                    'description' : listing.xpath(".//div[@class='content_31491']/p/text()").get(),
                    'website_url' : f'''https://www.producthunt.com{listing.xpath(".//a[@rel='noopener']/@href").get()}''',                
                    'tags' : listing.xpath(".//a[@class='postTopicLink_a090c']/span/text()").get(),
                    'votes' : listing.xpath(".//button/span/span/text()").get()
                }    


        # CODE TO FETCH THE CATEGORY URLs
        # listings = response_obj.xpath("//div[@class='item_56e23']")
        # for listing in listings:
        #     yield{
        #         'cat_urls': f'''https://www.producthunt.com{listing.xpath(".//a/@href").get()}''',
        #         'tag_name': listing.xpath(".//a/span/text()").get()
        #     }