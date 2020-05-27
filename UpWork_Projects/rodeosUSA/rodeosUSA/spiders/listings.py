# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector
import time


class ListingsSpider(scrapy.Spider):
    name = 'listings'
    
    def start_requests(self):
        yield SeleniumRequest(
            url="https://rodeosusa.com/rodeos/",
            wait_time=10,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        driver.set_window_size(1920, 1020)

        html = driver.page_source
        response_obj = Selector(text=html)
        titles = response_obj.xpath("//div[@class='one-half']/a[@itemprop='url']")
        for title in titles:
            title_url = title.xpath(".//@href").get()
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])
            driver.get(title_url)
            time.sleep(10)

            html1 = driver.page_source
            response_obj1 = Selector(text=html1)

            yield {
                'date': response_obj1.xpath("(//ul[@class='event-info'])[1]/li/span/text()").getall(),
                'directions': response_obj1.xpath("//div[text()='Directions']/following-sibling::div/a/text()").get(),
                'city_state': response_obj1.xpath("//div[text()='City/State']/following-sibling::div[1]/text()").get(),
                'directions': response_obj1.xpath("//div[text()='Directions']/following-sibling::div/a/text()").get(),
                'directions': response_obj1.xpath("//div[text()='Directions']/following-sibling::div/a/text()").get(),
                'directions': response_obj1.xpath("//div[text()='Directions']/following-sibling::div/a/text()").get(),
            }
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(5)



