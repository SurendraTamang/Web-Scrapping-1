# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy import Selector
import time


class LinkExtractSpider(scrapy.Spider):
    name = 'link_extract'
    cntr = 1
    lists = [
        'Bedding',
        'Bath'
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
        time.sleep(20)

        html = driver.page_source
        resp_obj = Selector(text=html)

        for i in self.lists:
            lvl1_list = resp_obj.xpath(f"//*[@id='tabPanel0']/div/div/section/div/div[1]/section[{self.cntr}]/div/div/a")
            self.cntr += 1
            for lvl1 in lvl1_list:
                lvl1_cat = i
                lvl2_cat = lvl1.xpath("normalize-space(.//text())").get()
                url = f'''https://www.bedbathandbeyond.com{lvl1.xpath(".//@href").get()}'''
                yield{
                    'lvl1_cat': lvl1_cat,
                    'lvl2_cat': lvl2_cat,
                    'url': url
                }
