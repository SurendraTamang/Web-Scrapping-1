# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector    
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.keys import Keys


class ExampleSpider(scrapy.Spider):
    name = 'example'

    def start_requests(self):
        yield SeleniumRequest(
            url="https://duckduckgo.com",
            wait_time=5,
            screenshot=True,
            callback=self.parse
        )

    def parse(self, response):
        # img = response.request.meta['screenshot']

        # with open('screenshot.png', 'wb') as f:
        #     f.write(img)

        driver = response.meta['driver']
        driver.set_window_size(1920, 1080)
        search_input = driver.find_element_by_id("search_form_input_homepage")
        search_input.send_keys("hello world")
        #driver.save_screenshot("search_key.png")
        search_input.send_keys(Keys.ENTER)
        #driver.save_screenshot("search_result.png")

        html = driver.page_source
        response_obj = Selector(text=html)

        links = response_obj.xpath("//div[@class='result__extras__url']/a")
        for link in links:
            yield {
                'URL': link.xpath(".//@href").get()
            }
