# -*- coding: utf-8 -*-
import scrapy
import time
import pandas as pd
from scrapy import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


class LinkextractSpider(scrapy.Spider):
    name = 'linkExtract'

    # df = pd.read_excel("D:/Web-Scrapping/UpWork_Projects/andy_upwork/dicksSportingGoods/lvl1.xlsx", sheet_name="lvl1")

    def start_requests(self):
        pass
        # yield SeleniumRequest(
        #     url="https://www.google.com",
        #     wait_time=6,
        #     callback=self.parse
        # )
    
    #       LINK EXTRACTOR FOR PAGE 1       #
    # def parse(self, response):
    #     driver = response.meta['driver']
    #     driver.maximize_window()
    #     time.sleep(10)

    #     action = ActionChains(driver)
    #     main_cat = driver.find_element_by_xpath("//span[text()='Shop Departments']")
    #     action.move_to_element(main_cat).perform()
    #     time.sleep(2)
    #     sub_cat = driver.find_element_by_xpath("//span[text()='Gift Guide']")
    #     action.move_to_element(sub_cat).perform()
    #     time.sleep(4)
    #     html = driver.page_source
    #     resp_obj = Selector(text=html)
    #     listings = resp_obj.xpath("//a[@class='headline']")
    #     for lists in listings:
    #         yield{
    #             'lvl1_cat': 'Gift Guide',
    #             'lvl2_cat': lists.xpath("normalize-space(.//text())").get(),
    #             'url': f'''https://www.dickssportinggoods.com{lists.xpath(".//@href").get()}'''
    #         }

    
    
    #       LINK EXTRACTOR FOR PAGE 2       #

    # def parse(self, response):
    #     driver = response.meta['driver']
    #     driver.maximize_window()

    #     for _, value in self.df.iterrows():
    #         driver.get(value['url'])
    #         time.sleep(5)

    #         try:
    #             WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//a[@_ngcontent-c28]")))
    #         except:
    #             pass
    #         html = driver.page_source
    #         resp_obj = Selector(text=html)

    #         check = resp_obj.xpath("//a[@_ngcontent-c28]")
    #         if check:
                
    #             expand = resp_obj.xpath("//div[contains(@class, 'overflow-category')]//span[contains(@class, 'mat-expansion-indicator')]")
    #             if expand:
    #                 for i in range(1, len(expand)+1):
    #                     driver.find_element_by_xpath(f"(//div[contains(@class, 'overflow-category')]//span[contains(@class, 'mat-expansion-indicator')])[{i}]").click()
    #                     time.sleep(2)
    #             else:
    #                 pass
                
    #             time.sleep(2)
    #             html = driver.page_source
    #             resp_obj = Selector(text=html)

    #             lvl2_listings = resp_obj.xpath("//a[@_ngcontent-c28]")
    #             for lvl2 in lvl2_listings:
    #                 lvl3_cat = lvl2.xpath(".//@title").get()
    #                 url = f'''https://www.dickssportinggoods.com{lvl2.xpath(".//@href").get()}'''
    #                 if lvl3_cat:
    #                     yield{
    #                         'lvl1_cat' : value['lvl1_cat'],
    #                         'lvl2_cat' : value['lvl2_cat'],
    #                         'lvl3_cat': lvl3_cat,
    #                         'url': url
    #                     }
    #         else:
    #             yield{
    #                 'lvl1_cat' : value['lvl1_cat'],
    #                 'lvl2_cat' : value['lvl2_cat'],
    #                 'lvl3_cat' : None,
    #                 'url' : value['url'],
    #             }