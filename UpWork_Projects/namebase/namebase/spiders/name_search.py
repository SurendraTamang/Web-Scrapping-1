# -*- coding: utf-8 -*-
import scrapy
from selenium.webdriver.common.keys import Keys
from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector
import time


class NameSearchSpider(scrapy.Spider):
    name = 'name_search'
    # allowed_domains = ['namebase.io']
    # start_urls = ['http://namebase.io/']

    params = [
        'analyse',
        'unite',
        'nb',
        'society',
        'google',
        'depressed'
    ]

    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.namebase.io/domains",
            wait_time=6,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        for item in self.params:
            search_box = driver.find_element_by_xpath("//input[@placeholder='Search for your personal TLD']")
            search_box.send_keys(item)
            #time.sleep(2)
            search_box.send_keys(Keys.ENTER)
            time.sleep(3)

            html = driver.page_source
            response = Selector(text=html)

            if response.xpath("//div[@class='desktop-bid-card']"):
                status = "Live"
                text = None
                days = response.xpath("//div[text()='Time left to bid (est.)']/preceding-sibling::div/text()").get()
                blocks = response.xpath("//div[text()='Blocks left to bid']/preceding-sibling::div/text()").get()
            elif response.xpath("//div[text()='Buy now']"):
                status = "Buy Now"
                text = response.xpath("//div[text()='HNS']/text()").get()
                days = None
                blocks = None
            elif response.xpath("//div[text()='Auction over']"):
                status = "Auction Over"
                text = response.xpath("//div[text()='Auction over']/following-sibling::div/text()").get()
                days = None
                blocks = None
            elif response.xpath("//div[text()='Already taken']"):
                status = "Already Taken"
                text = response.xpath("//div[text()='Already taken']/following-sibling::div/text()").get()
                days = None
                blocks = None
            elif response.xpath("//div[text()='Coming soon']"):
                status = "Coming Soon"
                text = response.xpath("//div[text()='Coming soon']/following-sibling::div/text()").get()
                days = response.xpath("//div[text()='Available in (est.)']/preceding-sibling::div/text()").get()
                blocks = response.xpath("//div[text()='Blocks until release']/preceding-sibling::div/text()").get()

            yield{
                'Word': item,
                'Status': status,
                'Text': text,
                'Blocks': blocks,
                'Days': days
            }     

            back_button = driver.find_element_by_xpath("//a[text()='Top-level domain']")
            back_button.click()
            time.sleep(3)