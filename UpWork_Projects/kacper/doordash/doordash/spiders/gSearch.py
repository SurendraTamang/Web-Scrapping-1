import scrapy
from scrapy import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
import time
import pandas as pd
from urllib.parse import unquote
import random


class GsearchSpider(scrapy.Spider):
    name = 'gSearch'

    df = pd.read_excel("./splitData.xlsx")
    cntr = 1

    def extractUrl(self, rawUrl):
        try:
            url = rawUrl.split("&url=")[-1].split("&")[0]
            return unquote(url).split("?utm_source=")[0]
        except:
            return None
    
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

        for _,val in self.df.iterrows():
            #try:
            self.cntr += 1
            if self.cntr % 14 == 0:
                driver.refresh()
                time.sleep(random.randint(5,10))
            WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='g']")))

            #   SEARCHING FOR THE QUERY STRING  #
            inputElem = driver.find_element_by_xpath("//input[@title='Search']")
            inputElem.clear()
            inputElem.send_keys(val['gSearchQuery'])

            serachBtnElem = driver.find_element_by_xpath("//button[@type='submit']")
            driver.execute_script("arguments[0].click()", serachBtnElem)

            time.sleep(1)
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='g']")))

            html = driver.page_source
            respObj = Selector(text=html)

            website = respObj.xpath("//div[text()='Website']/parent::a/@href").get()
            phone = respObj.xpath("normalize-space(//span[contains(@aria-label, 'phone number')]/text())").get()
            if not website:
                website = respObj.xpath("//div[text()='Website']/parent::div/parent::a/@href").get()
            if not phone:
                phone = respObj.xpath("normalize-space((//div[text()='Website']/parent::div/parent::a/preceding-sibling::a)[1]//span[contains(@class,'details')]/div[2]/span[last()]/text())").get()
            if not phone:    
                phone = respObj.xpath("normalize-space((//div[text()='Website']/parent::div/parent::a/preceding-sibling::a)[1]//span[contains(@class,'details')]/div[3]/span[last()]/text())").get()
            yield {
                'Id': val['Id'],
                'City': val['State'],
                'Area': val['City'],
                'Restaurant Name': val['Restaurant name'],
                'Average Rating': val['Average rating'],
                'Number Of Reviews': val['Number of reviews'],
                'Search Queries': val['gSearchQuery'],
                'Website': self.extractUrl(website),
                'Phone': phone
            }
            # except:
            #     pass