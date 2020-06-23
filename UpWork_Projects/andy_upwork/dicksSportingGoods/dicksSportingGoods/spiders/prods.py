# -*- coding: utf-8 -*-
import scrapy
import time
import pandas as pd
from scrapy import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class ProdsSpider(scrapy.Spider):
    name = 'prods'

    df = pd.read_excel("D:/Web-Scrapping/UpWork_Projects/andy_upwork/dicksSportingGoods/finalLinks.xlsx")
    
    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.google.com",
            wait_time=5,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        driver.maximize_window()

        for _, value in self.df.iterrows():
            driver.get(value['url'])
            time.sleep(5)
            try:
                WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='card_image']")))
                driver.implicitly_wait(5)

                try:
                    driver.find_element_by_xpath("//a[text()=144]").click()
                except:
                    pass
                time.sleep(6)
                cntr = 0

                while True:
                    driver.execute_script("window.scrollTo(0, 6000);")
                    time.sleep(3)
                    html = driver.page_source
                    resp_obj = Selector(text=html)
                    tc_raw = resp_obj.xpath("//span[@class='rs-page-count-label']/text()").get()
                    total_count = int(tc_raw.strip(" Products"))
                    if total_count % 144 == 0:
                        check = total_count//144
                    else:
                        check = (total_count//144)+1
                    cntr += 1

                    listings = resp_obj.xpath("//div[contains(@class, 'product-card-content-container')]")
                    for prods in listings:
                        yield{
                            'product_name': prods.xpath("normalize-space(.//div[contains(@class, 'product_description')]/a/text())").get(),
                            'price': prods.xpath("normalize-space(.//span[@class='rs_final_regular_price' or @class='rs_final_price']/text())").get(),
                            'lvl1_cat': value['lvl1_cat'],
                            'lvl2_cat': value['lvl2_cat'],
                            'lvl3_cat': value['lvl3_cat'],
                            'url': f'''https://www.dickssportinggoods.com{prods.xpath(".//div[contains(@class, 'product_description')]/a/@href").get()}'''
                        }

                    if cntr < check:
                        driver.get(f"{value['url']}?pageSize=144&pageNumber={cntr}")
                        time.sleep(10)
                    else:
                        break
            except:
                pass
