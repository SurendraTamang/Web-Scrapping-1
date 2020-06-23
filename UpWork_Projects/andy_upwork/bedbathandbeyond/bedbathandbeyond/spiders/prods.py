# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy import Selector
import time
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class ProdsSpider(scrapy.Spider):
    name = 'prods'

    df = pd.read_excel("D:/sipun/Web-Scrapping/UpWork_Projects/andy_upwork/bedbathandbeyond/links.xlsx")

    def scroll(self, driver, timeout):
        scroll_pause_time = timeout

        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            driver.execute_script("window.scrollTo(0, 3000);")

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
            url="https://www.google.com",
            wait_time=6,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        driver.maximize_window()
        for _, value in self.df.iterrows():
            cntr = 1
            driver.get(value['url'])
            time.sleep(10)
            #self.scroll(driver, 12)
            
            
            # driver.execute_script("window.scrollTo(0, 600);")
            # time.sleep(4)
            # button = driver.find_element_by_xpath("f"//a[text()={cntr}]"")
            # driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', button)
            
            # driver.find_element_by_xpath("//span[text()='24 per page']/parent::button[@value='24']/parent::div").click()
            # time.sleep(5)
            # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='96 per page']"))).click()
            
            while True:                
                cntr += 1
                button = driver.find_element_by_xpath(f"//a[text()={cntr}]")
                driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', button)
                time.sleep(2)
                driver.execute_script("window.scrollTo(0, 3000);")
                time.sleep(6)
                html = driver.page_source
                resp_obj = Selector(text=html)

                listings = resp_obj.xpath("//article")
                for prod in listings:
                    yield{
                        'name': prod.xpath("normalize-space(.//div[@data-locator='product_tile_title']/a/text())").get(),
                        'price': prod.xpath("normalize-space(.//div[@data-locator='product_tile_price']/span/text())").get(),
                        'lvl1_cat': value['lvl1_cat'],
                        'lvl2_cat': value['lvl2_cat'],
                        'url': f'''https://www.bedbathandbeyond.com{prod.xpath("div[@data-locator='product_tile_title']/a/@href").get()}'''
                    }

                next_page = resp_obj.xpath(f"//a[text()={cntr}]")
                if next_page:
                    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, f"//a[text()={cntr}]"))).click()
                    time.sleep(8)
                    #driver.execute_script("window.scrollTo(0, 3000);")
                    





            
