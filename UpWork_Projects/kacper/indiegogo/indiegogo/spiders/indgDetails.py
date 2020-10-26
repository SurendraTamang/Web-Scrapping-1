# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
import pandas as pd


class IndgdetailsSpider(scrapy.Spider):
    name = 'indgDetails'

    df = pd.read_excel("/root/rrScrapers/indiegogo/links_title.xlsx", sheet_name="linode2")
    
    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.indiegogo.com",
            wait_time=5,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        driver.maximize_window()
        for _,value in self.df.iterrows():
            driver.get(value['Url'])
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'campaignOwnerName')]")))
            html = driver.page_source
            respObj = Selector(text=html)
            try:
                url = re.findall('''"website_url":"?(http[0-9\a-z:A-Z]*)"?,''', html)[0]
                furl = url.replace('"', "")
            except:
                furl = None
            yield{
                'Title': value['Title'],
                'Creator': respObj.xpath("normalize-space(//div[contains(@class, 'campaignOwnerName')]/text())").get(),
                'Backers': respObj.xpath("normalize-space(//span[contains(text(), 'backers')]/preceding-sibling::span[1]/text())").get(),
                'Money': respObj.xpath("normalize-space(//span[contains(@class,'amountSold t-h5')]/text())").get(),
                'Website': furl,
            }
