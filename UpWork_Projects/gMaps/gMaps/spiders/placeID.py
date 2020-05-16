# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd



class PlaceidSpider(scrapy.Spider):
    name = 'placeID'

    df = pd.read_excel('D:/upworkWorkspace/Testing/Photo sourcing with State address - List two.xlsx', sheet_name='test')

    search_item = [
        'Fort Zumwalt Park Missouri',
        'Forum Nature Area Missouri',
        'Founders Park Missouri',
        'Fountain Bluff Sports Complex Missouri',
        'Fountain Lakes Park Missouri'

    ]

    def start_requests(self):
        yield SeleniumRequest(
            url="https://developers.google.com/places/place-id",
            wait_time=10,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        driver.set_window_size(1366, 768)
        driver.execute_script("window.scrollBy(0,300);")
        driver.switch_to.frame(0)

        for _,value in self.df.iterrows():
            lat = str(value['lat'])            
            long = str(value['long'])
            place_name = value['name']
            query = value['query']

            driver.find_element_by_xpath("//input[@id='pac-input']").clear()
            search_input = driver.find_element_by_xpath("//input[@id='pac-input']")
            search_input.send_keys(query)
            time.sleep(2)
            search_input.send_keys(Keys.ARROW_DOWN)
            search_input.send_keys(Keys.ENTER)
            time.sleep(2) 

            html = driver.page_source
            response_obj = Selector(text=html)
            yield{
                'place_name': place_name,
                'latitude': lat,
                'longitude': long,
                'place_id': response_obj.xpath("//span[@id='place-id']/text()").get()
                #'place_name': response_obj.xpath("//span[@id='place-name']/text()").get()
            }
