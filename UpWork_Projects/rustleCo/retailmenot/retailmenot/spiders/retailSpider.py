# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class RetailspiderSpider(scrapy.Spider):
    name = 'retailSpider'
    url = "https://help.retailmenot.com/s"

    def filter_answer(self, value):
        answer = " ".join([i.strip() for i in value])
        return answer
    
    def start_requests(self):
        yield SeleniumRequest(
            url=self.url,
            wait_time=5,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        driver.maximize_window()

        html = driver.page_source
        resp_obj = Selector(text=html)

        listings = resp_obj.xpath("//div[contains(@class, 'cardContainer')]")
        for i in range(1, len(listings)+1):
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"(//div[contains(@class, 'cardContainer')])[{i}]"))).click()
            time.sleep(6)
            #WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'topicTitle')]")))
            html = driver.page_source
            resp_obj = Selector(text=html)

            category = resp_obj.xpath("normalize-space(//div[contains(@class, 'topicTitle')]/text())").get()
            articles = resp_obj.xpath("//a[text()='Read Article']")
            for j in range(1, len(articles)+1):
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"(//a[text()='Read Article'])[{j}]"))).click()
                time.sleep(5)
                html = driver.page_source
                resp_obj = Selector(text=html)
                yield{
                    'question': resp_obj.xpath("normalize-space(//h1/text())").get(),
                    'answer': self.filter_answer(resp_obj.xpath("//div[contains(@class, 'full long-text')]//div[contains(@class, 'uiOutputRichText')]/text()").getall()),
                    'url': driver.current_url,
                    'category': category,
                    'company': "retailmenot"
                }
                driver.execute_script("window.history.go(-1)")
                time.sleep(4)
            driver.execute_script("window.history.go(-1)")
            time.sleep(5)

