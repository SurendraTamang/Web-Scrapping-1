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

    df = pd.read_excel("D:/Web-Scrapping/UpWork_Projects/andy_upwork/bedbathandbeyond/urls.xlsx", sheet_name="main")

    # def scroll(self, driver, timeout):
    #     scroll_pause_time = timeout

    #     for _ in range(3):
    #         # Scroll down to bottom
    #         #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #         driver.execute_script("window.scrollTo(0, 8000);")

    #         # Wait to load page
    #         time.sleep(scroll_pause_time)

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
            time.sleep(5)            
            
            # driver.execute_script("window.scrollTo(0, 600);")
            # time.sleep(4)
            # button = driver.find_element_by_xpath(f"//a[text()={cntr}]")
            # driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', button)
            
            # driver.find_element_by_xpath("//span[text()='24 per page']/parent::button[@value='24']/parent::div").click()
            # time.sleep(5)
            # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='96 per page']"))).click()
            
            while True:                
                cntr += 1
                driver.execute_script("window.scrollTo(0, 8000);")
                time.sleep(3)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(6)
                html = driver.page_source
                resp_obj = Selector(text=html)

                listings = resp_obj.xpath("//article")
                for prod in listings:
                    yield{
                        'name': prod.xpath("normalize-space(.//div[@data-locator='product_tile_title']/a/text())").get(),
                        'price': prod.xpath("normalize-space(.//div[@data-locator='product_tile_price']/span/text())").get(),
                        'lvl1_cat': value['cat'],
                        'lvl2_cat': value['sub_cat'],
                        'url': f'''https://www.bedbathandbeyond.com{prod.xpath("div[@data-locator='product_tile_title']/a/@href").get()}'''
                    }

                next_page = resp_obj.xpath(f"//a[text()={cntr}]")
                if next_page:
                    curr_url = driver.current_url
                    new_url = curr_url.replace(f"{cntr-1}-96", f"{cntr}-96")
                    driver.get(new_url)
                    del new_url
                    time.sleep(5)
                    #WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, f"//a[text()={cntr}]"))).click()
                    #time.sleep(8)
                    #driver.execute_script("window.scrollTo(0, 3000);")
                else:
                    break
                    





            
