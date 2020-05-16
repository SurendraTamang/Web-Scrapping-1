# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.keys import Keys
import time


class PlacesSpider(scrapy.Spider):
    name = 'places'

    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.google.com/maps",
            wait_time=10,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        driver.set_window_size(1366, 768)
        time.sleep(10)
        #driver.execute_script("window.scrollBy(0,300);")
        #driver.switch_to.frame(0)

        #for _,value in self.df.iterrows():
            # lat = str(value['lat'])            
            # long = str(value['long'])
            # place_name = value['name']
            # query = value['query']

        driver.find_element_by_xpath("//input[@id='gs_taif50']").clear()
        search_input = driver.find_element_by_xpath("//input[@id='pac-input']")
        search_input.send_keys("optical stores in bangalore")
        time.sleep(2)
        search_input.send_keys(Keys.ARROW_DOWN)
        search_input.send_keys(Keys.ENTER)
        time.sleep(10) 

        # html = driver.page_source
        # response_obj = Selector(text=html)
        yield{
            # 'place_name': place_name,
            # 'latitude': lat,
            # 'longitude': long,
            # 'place_id': response_obj.xpath("//span[@id='place-id']/text()").get()
            #'place_name': response_obj.xpath("//span[@id='place-name']/text()").get()
        }