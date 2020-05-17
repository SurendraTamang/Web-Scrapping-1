# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from scrapy.selector import Selector
import time


class IgscrapperSpider(scrapy.Spider):
    name = 'igScrapper'
    # allowed_domains = ['www.instagram.com']
    # start_urls = ['https://www.instagram.com/']

    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.instagram.com/",
            wait_time=6,
            callback=self.parse
        )
    
    def parse(self, response):
        driver = response.meta['driver']
        #chrome_options.add_argument("--headless")
        #chrome_options.add_extension("D:/WebScrapping/advancedWebScrapping/instaScrapper/Block-image_v1.1.crx") => Works on older chrome version
        #driver = webdriver.Chrome(executable_path="D:/sipun/Web-Scrapping/UpWork_Projects/gMaps/chromedriver.exe", options=chrome_options)
        driver.set_window_size(1920, 1080)
        #driver.get("https://www.instagram.com/")
        time.sleep(5)
        usr_name = driver.find_element_by_xpath("//input[@aria-label='Phone number, username, or email']")
        usr_name.send_keys("byomakesh.patra1993@gmail.com")
        psswd = driver.find_element_by_xpath("//input[@aria-label='Password']")
        psswd.send_keys("Sipun@199^")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(10)
        html = driver.page_source
        response = Selector(text=html)
        if response.xpath("//button[text()='Not Now']"):            
            driver.find_element_by_xpath("//button[text()='Not Now']").click()

        time.sleep(3)

        search_input_box = driver.find_element_by_xpath("//input[@placeholder='Search']")
        search_input_box.send_keys("oneplus")
        time.sleep(10)
        driver.find_element_by_xpath("//div[@class='fuqBx']/a[1]").click()
        time.sleep(10)