# -*- coding: utf-8 -*-
import scrapy
import time
import pandas as pd
from scrapy import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class DtproductsSpider(scrapy.Spider):
    name = 'dtProducts'
    # allowed_domains = ['www.dollartree.com']
    # start_urls = ['https://www.dollartree.com/']

    df = pd.read_excel("D:/sipun/Web-Scrapping/UpWork_Projects/andy_upwork/dollarTree/links.xlsx")

    def scroll(self, driver, timeout):
        scroll_pause_time = timeout

        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
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
            url="https://www.dollartree.com",
            wait_time=6,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        driver.maximize_window()
        for _, value in self.df.iterrows():
            try:
                driver.get(value['url'])
                WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "(//select[@class='form-control col-md-12 select'])[2]"))).click()
                WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "(//select[@class='form-control col-md-12 select'])[2]//option[text()='View All']"))).click()
                time.sleep(5)
                self.scroll(driver, 7)

                html = driver.page_source
                resp_obj = Selector(text=html)

                listings = resp_obj.xpath("//div[@class='product']")
                for lists in listings:
                    yield{
                        'product_url' : f'''https://www.dollartree.com{lists.xpath(".//div[@class='product-title']/a/@href").get()}''',
                        'product_name' : lists.xpath("normalize-space(.//div[@class='product-title']/a/span/text())").get(),
                        'lvl1_cat': value['lvl1_cat'],
                        'lvl2_cat': value['lvl2_cat'],
                        'lvl3_cat': value['lvl3_cat'],
                        'price' : f'''{lists.xpath("normalize-space(.//div[@class='minimum-to-buy']/span/text())").get()} @ {lists.xpath("normalize-space(//div[@class='product-item-price']/span[1]/text())").get()} {lists.xpath("normalize-space(//div[@class='product-item-price']/span[2]/text())").get()}'''
                    }
            except:
                pass
    
    
    
    # CODE FOR LINK EXTRACTION    
    
    # def parse(self, response):
    #     driver = response.meta['driver']
    #     driver.maximize_window()
    #     WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, "//span[text()='Shop By Department']")))
    #     time.sleep(10)

    #     html = driver.page_source
    #     resp_obj = Selector(text=html)

    #     listings = resp_obj.xpath("//span[text()='Shop By Department']/parent::a/following-sibling::ul[@class='dropdown-menu']/li")
    #     for lists in listings:
    #         lvl1_cat = lists.xpath(".//span[@data-bind='text: title']/parent::a/@title").get()
    #         lvl2_listings = lists.xpath(".//div[@class='menu-content']/div/li")
    #         for lvl2_lists in lvl2_listings:
    #             lvl2_cat = lvl2_lists.xpath(".//a/@title").get()
    #             url = f'''https://www.dollartree.com{lvl2_lists.xpath(".//a/@href").get()}'''

    #             driver.get(url)
    #             try:
    #                 WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, "//ul[@class='child-items']/li")))
    #                 html = driver.page_source
    #                 resp_obj = Selector(text=html)
                    
    #                 lvl3_listings = resp_obj.xpath("//ul[@class='child-items']/li")
    #                 for lvl3_lists in lvl3_listings:
    #                     url = f'''https://www.dollartree.com{lvl3_lists.xpath(".//a/@href").get()}'''
    #                     lvl3_cat = lvl3_lists.xpath(".//a/@title").get()
    #                     yield{
    #                         'lvl1_cat': lvl1_cat,
    #                         'lvl2_cat': lvl2_cat,
    #                         'lvl3_cat': lvl3_cat,
    #                         'url': url
    #                     }
    #             except:
    #                 yield{
    #                         'lvl1_cat': lvl1_cat,
    #                         'lvl2_cat': lvl2_cat,
    #                         'lvl3_cat': None,
    #                         'url': url
    #                     }

        
