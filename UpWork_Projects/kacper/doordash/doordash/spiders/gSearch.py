import scrapy
from scrapy import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
import time
import pandas as pd


class GsearchSpider(scrapy.Spider):
    name = 'gSearch'

    df = pd.read_excel("./data/doordashData-phase1.xlsx")
    
    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.google.com/search?client=firefox-b-d&q=googlesearch",
            wait_time=10,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']

        stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

        driver.maximize_window()

        WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='g']")))

        #   SEARCHING FOR THE QUERY STRING  #
        inputElem = driver.find_element_by_xpath("//input[@title='Search']")
        inputElem.clear()
        inputElem.send_keys("It's Just Wings,Alamogordo,Albuquerque")

        serachBtnElem = driver.find_element_by_xpath("//button[@type='submit']")
        driver.execute_script("arguments[0].click()", serachBtnElem)

        time.sleep(1)
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='g']")))

        html = driver.page_source
        respObj = Selector(text=html)

        yield {
            'Website': respObj.xpath("//div[text()='Website']/parent::a/@href").get(),
            'Phone': respObj.xpath("normalize-space(//span[contains(@aria-label, 'phone number')]/text())").get()
        }