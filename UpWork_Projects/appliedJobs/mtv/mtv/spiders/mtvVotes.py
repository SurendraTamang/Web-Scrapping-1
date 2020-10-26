import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


class MtvvotesSpider(scrapy.Spider):
    name = 'mtvVotes'

    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.mtvema.com",
            wait_time=5,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        driver.maximize_window()
        driver.get("https://www.mtvema.com/en-in/vote/")
        while True:
            WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//img[@alt='Prabh Deep']/parent::div/following-sibling::button"))).click()
            time.sleep(5)
