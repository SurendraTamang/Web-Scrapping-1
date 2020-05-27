# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.keys import Keys
from scrapy import Selector
import time
import pandas as pd


class LatlongSpider(scrapy.Spider):
    name = 'latLong'
    
    df = pd.read_excel("D:/sipun/Web-Scrapping/UpWork_Projects/gmaps_lat_long_scrapper/50_lat_long_places.xlsx")

    def filter_lat(self, value):
        try:
            filter = value.replace("Location: ","")
            li = list(map(str, filter.rstrip().split(",")))
            return str(li[0])
        except:
            return None

    def filter_long(self, value):
        try:
            filter = value.replace("Location: ","")
            li = list(map(str, filter.rstrip().split(",")))
            return str(li[1])
        except:
            return None

    def start_requests(self):
        yield SeleniumRequest(
            url="https://developers.google.com/maps/documentation/geocoding/intro",
            wait_time=6,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        driver.set_window_size(1366, 1080)
        driver.execute_script("window.scrollBy(0,500);")
        time.sleep(5)
        driver.switch_to.frame(0)

        for _,value in self.df.iterrows():
            search_param = value['query']
            driver.find_element_by_xpath("//input[@id='query-input']").clear()
            search_input = driver.find_element_by_xpath("//input[@id='query-input']")
            search_input.send_keys(search_param)
            search_input.send_keys(Keys.ENTER)
            time.sleep(4)

            html = driver.page_source
            response_obj = Selector(text=html)
            latlong = response_obj.xpath("normalize-space((//p[@class='result-location']/text())[3])").get()
            
            yield{
                "query": search_param,
                "latitude": self.filter_lat(latlong),
                "longitude": self.filter_long(latlong)
            }

