# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy import Selector
import time
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class WmproductsSpider(scrapy.Spider):
    name = 'wmProducts'

    df = pd.read_excel("D:/Web-Scrapping/UpWork_Projects/andy_upwork/wallmart/links_main.xlsx", sheet_name='test')
    
    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.walmart.com",
            wait_time=6,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        for _, value in self.df.iterrows():
            driver.get(value['url'])
            time.sleep(2)

            html = driver.page_source
            resp_obj = Selector(text=html)

            check1 = resp_obj.xpath("//div[@data-type='items']")
            check2 = resp_obj.xpath("//span[text()='Shop by Category' or text()='Shop by category']/parent::span/parent::button/following-sibling::div/div/ul/li")
            check3 = resp_obj.xpath("//h2[text()='Shop by category']/parent::div/parent::div/following-sibling::div//div[@class='TempoCategoryTile-tile valign-top']")
            if check1:
                cntr = 1
                while True:
                    html = driver.page_source
                    resp_obj = Selector(text=html)
                    listings = resp_obj.xpath("//div[@data-type='items']")
                    for prods in listings:
                        price = prods.xpath("normalize-space(.//span[@class='price-main-block']/span/span/text())").get()
                        if not price:
                            price = f'''{prods.xpath("normalize-space(.//span[@class='price price-main'][1]/span/text())").get()} - {prods.xpath("normalize-space(.//span[@class='price price-main'][2]/span/text())").get()}'''
                        yield {
                            'product_name': prods.xpath("normalize-space(.//div[@class='search-result-product-title gridview']/a/span/text())").get(),
                            'product_price': price,
                            'lvl1_cat': value['lvl1_cat'],
                            'lvl2_cat': value['lvl2_cat'],
                            'lvl3_cat': value['lvl3_cat'],
                            'lvl4_cat': None,
                            'product_url': f'''https://www.walmart.com{prods.xpath(".//div[@class='search-result-product-title gridview']/a/@href").get()}'''
                        }
                    
                    next_page = resp_obj.xpath("//span[text()='Next Page']/parent::button")
                    cntr += 1
                    if next_page:
                        next_page = resp_obj.xpath(f"//ul[@class='paginator-list']/li/a[text()='{cntr}']/@href").get()
                        driver.get(f"https://www.walmart.com{next_page}")
                        time.sleep(2)
                    else:
                        break

            elif check2:
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[1])
                for listings in check2:
                    lvl4_cat = listings.xpath(".//a/span/text()").get()
                    url = listings.xpath(".//a/@href").get()
                    driver.get(f"https://www.walmart.com{url}")
                    cntr = 1
                    while True:
                        html = driver.page_source
                        resp_obj = Selector(text=html)
                        listings = resp_obj.xpath("//div[@data-type='items']")
                        for prods in listings:
                            price = prods.xpath("normalize-space(.//span[@class='price-main-block']/span/span/text())").get()
                            if not price:
                                price = f'''{prods.xpath("normalize-space(.//span[@class='price price-main'][1]/span/text())").get()} - {prods.xpath("normalize-space(.//span[@class='price price-main'][2]/span/text())").get()}'''
                            yield {
                                'product_name': prods.xpath("normalize-space(.//div[@class='search-result-product-title gridview']/a/span/text())").get(),
                                'product_price': price,
                                'lvl1_cat': value['lvl1_cat'],
                                'lvl2_cat': value['lvl2_cat'],
                                'lvl3_cat': value['lvl3_cat'],
                                'lvl4_cat': lvl4_cat,
                                'product_url': f'''https://www.walmart.com{prods.xpath(".//div[@class='search-result-product-title gridview']/a/@href").get()}'''
                            }
                        
                        next_page = resp_obj.xpath("//span[text()='Next Page']/parent::button")
                        cntr += 1
                        if next_page:
                            next_page = resp_obj.xpath(f"//ul[@class='paginator-list']/li/a[text()='{cntr}']/@href").get()
                            driver.get(f"https://www.walmart.com{next_page}")
                            time.sleep(2)
                        else:
                            break
                driver.close()
                driver.switch_to.window(driver.window_handles[0])

            elif check3:
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[1])
                for listings in check3:
                    lvl4_cat = listings.xpath(".//span/text()").get()
                    url = listings.xpath(".//following-sibling::a/@href").get()
                    driver.get(f"https://www.walmart.com{url}")
                    cntr = 1
                    while True:
                        html = driver.page_source
                        resp_obj = Selector(text=html)
                        listings = resp_obj.xpath("//div[@data-type='items']")
                        for prods in listings:
                            price = prods.xpath("normalize-space(.//span[@class='price-main-block']/span/span/text())").get()
                            if not price:
                                price = f'''{prods.xpath("normalize-space(.//span[@class='price price-main'][1]/span/text())").get()} - {prods.xpath("normalize-space(.//span[@class='price price-main'][2]/span/text())").get()}'''
                            yield {
                                'product_name': prods.xpath("normalize-space(.//div[@class='search-result-product-title gridview']/a/span/text())").get(),
                                'product_price': price,
                                'lvl1_cat': value['lvl1_cat'],
                                'lvl2_cat': value['lvl2_cat'],
                                'lvl3_cat': value['lvl3_cat'],
                                'lvl4_cat': lvl4_cat,
                                'product_url': f'''https://www.walmart.com{prods.xpath(".//div[@class='search-result-product-title gridview']/a/@href").get()}'''
                            }
                        
                        next_page = resp_obj.xpath("//span[text()='Next Page']/parent::button")
                        cntr += 1
                        if next_page:
                            next_page = resp_obj.xpath(f"//ul[@class='paginator-list']/li/a[text()='{cntr}']/@href").get()
                            driver.get(f"https://www.walmart.com{next_page}")
                            time.sleep(2)
                        else:
                            break
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                
            else:
                pass
                
