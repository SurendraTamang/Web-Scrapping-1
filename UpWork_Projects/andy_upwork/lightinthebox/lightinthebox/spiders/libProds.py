# -*- coding: utf-8 -*-
import scrapy
import time
import pandas as pd
from scrapy import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class LibprodsSpider(scrapy.Spider):
    name = 'libProds'

    df = pd.read_excel("D:/sipun/Web-Scrapping/UpWork_Projects/andy_upwork/lightinthebox/links_new.xlsx", sheet_name="urls")

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
            url="https://www.lightinthebox.com",
            wait_time=6,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        driver.maximize_window()
        WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, "//ul[@class='line-16']/li//h2")))
        time.sleep(30)
        for _, value in self.df.iterrows():
            try:
                driver.get(value['url'])
                WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, "//dl[contains(@class, 'item-block')]//dd[@class='prod-name']")))
                
                while True:
                    self.scroll(driver, 3)
                    html = driver.page_source
                    resp_obj = Selector(text=html)
                    listings = resp_obj.xpath("//dl[contains(@class, 'item-block')]")
                    for lists in listings:
                        yield{
                            'product_name': lists.xpath("normalize-space(.//dd[@class='prod-name']/a/@title)").get(),
                            'price': lists.xpath("normalize-space(.//dd/a[contains(@class, 'price')]/text())").get(),
                            'lvl1_cat': value['lvl1_cat'],
                            'lvl2_cat': value['lvl2_cat'],
                            'lvl3_cat': value['lvl3_cat'],
                            'url': lists.xpath(".//dd[@class='prod-name']/a/@href").get()
                        }

                    next_page = resp_obj.xpath("//span[text()='Next']")
                    if next_page:
                        driver.find_element_by_xpath("//span[text()='Next']").click()
                        time.sleep(5)
                    else:
                        break
            except:
                yield{
                    'product_name': 'FAILED',
                    'price': None,
                    'lvl1_cat': value['lvl1_cat'],
                    'lvl2_cat': value['lvl2_cat'],
                    'lvl3_cat': value['lvl3_cat'],
                    'url': value['url']
                }


                                          #    CODE FOR URL EXTRACTION    #   

    # def parse(self, response):
    #     driver = response.meta['driver']
    #     driver.maximize_window()
    #     WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, "//ul[@class='line-16']/li//h2")))
    #     time.sleep(20)
        
    #     html_lvl1 = driver.page_source
    #     resp_obj_lvl1 = Selector(text=html_lvl1)
    #     lvl1_listings = resp_obj_lvl1.xpath("//ul[@class='line-16']/li")
    #     for lvl1_list in lvl1_listings:
    #         #lvl1_url = lvl1_list.xpath(".//h2/a/@href").get()
    #         lvl1_cat = lvl1_list.xpath("normalize-space(.//h2/a/text())").get()            
    #         lvl2_listings = lvl1_list.xpath(".//div[@class='c-m-sub']/child::dl")
    #         for lvl2_list in lvl2_listings:
    #             lvl2_cat = lvl2_list.xpath("normalize-space(.//h3/a/text())").get()
    #             lvl3_listings = lvl2_list.xpath(".//dd/a")
    #             for lvl3_list in lvl3_listings:
    #                 lvl3_cat = lvl3_list.xpath(".//text()").get()
    #                 url = lvl3_list.xpath(".//@href").get()

    #                 yield{
    #                     'lvl1_cat': lvl1_cat,
    #                     'lvl2_cat': lvl2_cat,
    #                     'lvl3_cat': lvl3_cat,
    #                     'url': url
    #                 }


