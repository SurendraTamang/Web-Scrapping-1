import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy import Selector
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


class WmcapspiderSpider(scrapy.Spider):
    name = 'wmCapSpider'
    
    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.walmart.com/receipt-lookup",
            wait_time=5,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        driver.maximize_window()
        time.sleep(40)
