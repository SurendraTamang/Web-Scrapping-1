# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy import Selector
import time


class LinkExtractSpider(scrapy.Spider):
    name = 'link_extract'
    cntr = 3
    lvl1_cat = [
        'Kitchen',
        'Dining',
        'Outdoor',
        'Baby & Kids',
        'Home Decor',
        'Furniture',
        'Curtain & Window',
        'Storage & Cleaning',
        'Smart Home & Home Improvement',
        'Health & Beauty',
        'Laugage, Pet & More',
        'Gifts',
        'Personalize & Monogram',
        'Holoday'
    ]

    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.bedbathandbeyond.com",
            wait_time=7,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        driver.maximize_window()
        time.sleep(10)

        html = driver.page_source
        resp_obj = Selector(text=html)

        # for i, cat in zip(range(3,17), self.lvl1_cat):
        #listings = resp_obj.xpath(f"//div[@id='top-nav-menu']/div[1]/div[2]//div[@class='MegaMenu_142Ng4']/section[1]/div/div[1]/section[{i}]/div[@class='MenuPanel_4R5iRr']/div/a")
        for cat in self.lvl1_cat:
            listings = resp_obj.xpath(f"//div[@id='top-nav-menu']/div[1]/div[2]//div[@class='MegaMenu_142Ng4']/section[1]/div/div[1]/section[{self.cntr}]/div[@class='MenuPanel_4R5iRr']/div/a")
            self.cntr += 1
            for lists in listings:
                yield{
                    'url': f'''https://www.bedbathandbeyond.com/{lists.xpath(".//@href").get()}''',
                    'lvl1_cat': cat,
                    'lvl2_cat': lists.xpath(".//text()").get()
                }
