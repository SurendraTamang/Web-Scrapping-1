# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class WishproductsSpider(scrapy.Spider):
    name = 'wishProducts'
    cntr = 0

    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.wish.com/feed/tag_53e9157121a8633c567eb0c2",
            wait_time=6,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        driver.maximize_window()

        # User Login
        email = driver.find_element_by_xpath("(//input[@data-id='emailAddress'])[2]")
        email.send_keys("byomakesh.patra1993@gmail.com")
        passwd = driver.find_element_by_xpath("(//input[@data-id='password'])[2]")
        passwd.send_keys("Sipun1996")
        driver.find_element_by_xpath("//div[text()='Forgot password?']/following-sibling::div").click()
        WebDriverWait(driver, 1000).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'ProductGrid__Wrapper')]/div/div[@data-index=1]//div[@class='ProductGrid__FeedTileWidthWrapper-sc-1luslvl-2 iLdHN'][4]//img")))
        time.sleep(20)
        # html = driver.page_source
        # resp_obj = Selector(text=html)

        # Extraction of product info
        while True:
            for i in range(1,5):
                try:
                    driver.find_element_by_xpath(f"//div[contains(@class, 'ProductGrid__Wrapper')]/div/div[@data-index={self.cntr}]//div[@class='ProductGrid__FeedTileWidthWrapper-sc-1luslvl-2 iLdHN'][{i}]//img").click()
                    WebDriverWait(driver, 120).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'PurchaseContainer__UpperWrapper')]/h1")))
                    time.sleep(1)
                    html = driver.page_source
                    resp_obj = Selector(text=html)
                    yield{
                        'product_name': resp_obj.xpath("//div[contains(@class, 'PurchaseContainer__UpperWrapper')]/h1/text()").get(),
                        'price': resp_obj.xpath("//div[contains(@class, 'PurchaseContainer__ActualPrice')]/text()").get(),
                        'category': "Home Decor",
                        'url': driver.current_url
                    }
                
                    driver.execute_script("window.history.go(-1)")
                    time.sleep(3)
                except:
                    pass
            self.cntr += 1
            
            # To handle infinite scrolling
            if self.cntr % 5 == 0:
                self.last_height = driver.execute_script("return document.body.scrollHeight")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(6)
                self.new_height = driver.execute_script("return document.body.scrollHeight")
                if self.new_height == self.last_height:
                    break
                self.last_height = self.new_height
