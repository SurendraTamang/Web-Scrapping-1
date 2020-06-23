# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy import Selector
import time


class LinkextractSpider(scrapy.Spider):
    name = 'linkExtract'
    # allowed_domains = ['www.wallmart.com']
    # start_urls = ['http://www.wallmart.com/']

    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.walmart.com/cp/toys/4171?&povid=4171+%7C+contentZone20+%7C+2016-11-08+%7C+1+%7C+Toys+Flyout",
            wait_time=6,
            callback=self.parse
        )

    def parse(self, response):
        lvl1_cat = 'Toys'
        driver = response.meta['driver']
        driver.maximize_window()
        time.sleep(25)

        html = driver.page_source
        resp_obj = Selector(text=html)

        list1 = resp_obj.xpath("(//ul[@class='block-list module no-margin'])[1]//li[@class='SideBarMenuModuleItem']")
        # driver.execute_script("window.open('');")
        # driver.switch_to.window(driver.window_handles[1])
        for lists in list1:
            #url1 = f'''https://www.walmart.com{lists.xpath(".//a/@href").get()}'''
            lvl2_cat = lists.xpath("normalize-space(.//a/span/text())").get()
            
            # driver.get(url1)
            # time.sleep(4)

            # html_new = driver.page_source
            # resp_obj_new = Selector(text=html_new)

            list2 = lists.xpath(".//ul[@class='block-list pull-left']/li")
            print(list2)
            for lists_new in list2:
                yield{
                    'lvl1_cat': lvl1_cat,
                    'lvl2_cat': lvl2_cat,
                    'lvl3_cat': lists_new.xpath("normalize-space(.//a/text())").get(),
                    'url': f'''https://www.walmart.com{lists_new.xpath(".//a/@href").get()}'''
                }

