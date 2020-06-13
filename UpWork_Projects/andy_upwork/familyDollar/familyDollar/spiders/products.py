# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd


class ProductsSpider(scrapy.Spider):
    name = 'products'

    df = pd.read_excel("D:/sipun/Web-Scrapping/UpWork_Projects/familyDollar/urls_list.xlsx")

    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.familydollar.com",
            wait_time=3,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        driver.maximize_window()

        for _, val in self.df.iterrows():
            category = val['category']
            sub_category = val['sub_category']
            sub_category_url = val['sub_category_url']
            cntr = 2
            driver.get(sub_category_url)
            try:
                WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='section view-all ib']//img"))).click()
            except:
                pass
            try:
                WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "(//div[@class='oc3-select']//select)[2]"))).click()
                time.sleep(2)
                driver.find_element_by_xpath("(//div[@class='oc3-select']//select)[2]/option[text()='96 per page']").click()
                time.sleep(10)      

                while True:
                    html = driver.page_source
                    response_obj = Selector(text=html)

                    listings = response_obj.xpath("//div[@class='product']/div[@class='product-title']")
                    for lists in listings:
                        yield{
                            'product_name': lists.xpath("normalize-space(.//a/span/text())").get(),
                            'category': category,
                            'sub-category': sub_category,
                            'product_url': f'https://www.familydollar.com{lists.xpath("normalize-space(.//a/@href)").get()}'
                        }

                    if response_obj.xpath(f"//a[text()='{cntr}']"):
                        driver.find_element_by_xpath(f"//a[text()='{cntr}']").click()
                        time.sleep(10)
                    else:
                        break
                    cntr += 1

            except:
                pass
            