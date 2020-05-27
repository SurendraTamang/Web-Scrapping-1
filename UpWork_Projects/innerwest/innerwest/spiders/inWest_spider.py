# -*- coding: utf-8 -*-
import scrapy
import time
from selenium.webdriver.common.action_chains import ActionChains
from scrapy_selenium import SeleniumRequest


class InwestSpiderSpider(scrapy.Spider):
    name = 'inWest_spider'

    def scroll(self, driver, timeout):
        scroll_pause_time = timeout
        cntr = 0

        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        while cntr != 500:
            print(cntr)
            cntr += 1
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(scroll_pause_time)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                # If heights are the same it will exit the function
                break
            last_height = new_height
    
    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.innerwest.nsw.gov.au/about/get-in-touch/online-self-service",
            wait_time=6,
            callback=self.main_page
        )

    def main_page(self, response):
        driver = response.meta['driver']
        driver.set_window_size(1366, 1080)
        driver.find_element_by_xpath("//a[text()='Enter as a guest']").click()
        time.sleep(7)
        driver.find_element_by_xpath("(//a[@class='hyperlink'])[3]").click()
        time.sleep(15)
        
        scroll_element = driver.find_element_by_xpath("//div[@class='views']")
        driver.execute_script('arguments[0].scrollIntoView(true);', scroll_element)
        
        # actions = ActionChains(driver)
        # actions.click_and_hold(scroll_element)

        time.sleep(1)
        self.scroll(driver,6)

    def parse(self, response):
        pass
