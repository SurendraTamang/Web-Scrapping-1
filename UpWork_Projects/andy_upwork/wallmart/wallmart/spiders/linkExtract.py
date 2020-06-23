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
            url='''https://www.walmart.com/cp/baby-products/5427?povid=BabyGlobalNav_ShopAllBaby''',
            wait_time=6,
            callback=self.parse
        )

    def parse(self, response):
        lvl1_cat = 'Kids'
        driver = response.meta['driver']
        driver.maximize_window()
        time.sleep(4)

        html = driver.page_source
        resp_obj = Selector(text=html)

        list1 = resp_obj.xpath("//span[text()='Shop by Category']/parent::span/parent::button/parent::div//ul[@class='block-list module no-margin']//li[@class='SideBarMenuModuleItem']")
        #list1 = resp_obj.xpath("//span[text()='Jewelry & Watches']/parent::span/parent::button/parent::div//ul[@class='block-list module no-margin']//li[@class='SideBarMenuModuleItem']")
        # driver.execute_script("window.open('');")
        # driver.switch_to.window(driver.window_handles[1])
        for lists in list1:
            #url1 = f'''https://www.walmart.com{lists.xpath(".//a/@href").get()}'''
            lvl2_cat = lists.xpath("normalize-space(.//a/span/text())").get()
            lvl2_url = lists.xpath("normalize-space(.//a/@href)").get()
            
            # driver.get(url1)
            # time.sleep(4)

            # html_new = driver.page_source
            # resp_obj_new = Selector(text=html_new)

            list2 = lists.xpath(".//ul[@class='block-list pull-left']/li")
            if list2:
                #print(list2)
                for lists_new in list2:
                    url = lists_new.xpath(".//a/@href").get()
                    if not url.startswith("https", 0, 5):
                        url = f'''https://www.walmart.com{lists_new.xpath(".//a/@href").get()}'''
                    yield{
                        'lvl1_cat': lvl1_cat,
                        'lvl2_cat': lvl2_cat,
                        'lvl3_cat': lists_new.xpath("normalize-space(.//a/text())").get(),
                        'url': url
                    }
            else:
                if not lvl2_url.startswith("https", 0, 5):
                    lvl2_url = f'''https://www.walmart.com{lvl2_url}'''
                yield{
                        'lvl1_cat': lvl1_cat,
                        'lvl2_cat': lvl2_cat,
                        'lvl3_cat': lvl2_cat,
                        'url': lvl2_url
                    }

