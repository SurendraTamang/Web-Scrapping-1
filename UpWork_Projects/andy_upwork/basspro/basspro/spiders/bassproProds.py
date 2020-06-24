# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
from scrapy import Selector
from scrapy_selenium import SeleniumRequest
import time


class BassproprodsSpider(scrapy.Spider):
    name = 'bassproProds'

    df = pd.read_excel("D:/Web-Scrapping/UpWork_Projects/andy_upwork/basspro/links.xlsx", sheet_name='links')
    
    # def extractURL(self, value):
    #     start = value.find("'https") + len("'https")
    #     end = value.find("')")
    #     substring = value[start:end]
    #     return f"https{substring}"

    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.basspro.com/shop/en",
            wait_time=5,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        driver.maximize_window()

        for _, value in self.df.iterrows():
            driver.get(value['url'])
            time.sleep(15)

            try:
                cntr = 2
                while True:
                    # driver.execute_script("window.scrollTo(0, 900);")
                    # time.sleep(1)
                    html = driver.page_source
                    resp_obj = Selector(text=html)

                    listings = resp_obj.xpath("//ul[@class='grid_mode grid']/li")
                    for prods in listings:
                        price = prods.xpath("normalize-space(.//span[@class='price sale']/span/text())").get()
                        if not price:
                            price = prods.xpath("normalize-space(.//span[@class='price ']/span/text())").get()
                        yield {
                            'productName': prods.xpath("normalize-space(.//div[@class='product_name']/a/text())").get(),
                            'price': price,
                            'lvl1_cat': value['lvl1_cat'],
                            'lvl2_cat': value['lvl2_cat'],
                            'lvl3_cat': value['lvl3_cat'],
                            'url': prods.xpath(".//div[@class='product_name']/a/@href").get()
                        }

                    next_page = resp_obj.xpath(f"//div[@class='pageControl number']//a[text()={cntr}]")
                    if next_page:
                        driver.execute_script("window.scrollTo(0, 600);")
                        #driver.find_element_by_xpath(f"//div[@class='pageControl number']//a[text()='{cntr}']").click()
                        cntr += 1
                        time.sleep(6)
                    else:
                        break

            except:
                yield {
                    'productName': 'Failed',
                    'price': 'Failed',
                    'lvl1_cat': value['lvl1_cat'],
                    'lvl2_cat': value['lvl2_cat'],
                    'lvl3_cat': value['lvl3_cat'],
                    'url': value['url']
                }


    #       CODE FOR EXTRACTING LINKS       #

    # def parse(self, response):
    #     driver = response.meta['driver']
    #     driver.maximize_window()
    #     time.sleep(3)

    #     html = driver.page_source
    #     resp_obj = Selector(text=html)

    #     lvl1_listing = resp_obj.xpath("//a[@class='departmentButton' and @role='menuitem']/parent::li")
    #     for lvl1 in lvl1_listing:
    #         lvl1_cat = lvl1.xpath("normalize-space(.//a[@class='departmentButton' and @role='menuitem']/text()[2])").get()
    #         lvl2_listing = lvl1.xpath(".//ul[@class='categoryList']/li")
    #         for lvl2 in lvl2_listing:
    #             lvl2_cat = lvl2.xpath("normalize-space(.//ul[@class='subcategoryList']/preceding-sibling::a/text())").get()
    #             lvl3_listings = lvl2.xpath(".//ul[@class='subcategoryList']/li")
    #             for lvl3 in lvl3_listings:
    #                 lvl3_cat = lvl3.xpath("normalize-space(.//a/text())").get()
    #                 url = self.extractURL(lvl3.xpath(".//a/@onclick").get())

    #                 yield{
    #                     'lvl1_cat': lvl1_cat,
    #                     'lvl2_cat': lvl2_cat,
    #                     'lvl3_cat': lvl3_cat,
    #                     'url': url
    #                 }
