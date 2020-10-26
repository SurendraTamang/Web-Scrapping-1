import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy import Selector
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


class GnewsspiderSpider(scrapy.Spider):
    name = 'gnewsSpider'

    keywords = [
        'https://news.google.com/search?q=iphone&hl=en-IN&gl=IN&ceid=IN%3Aen',
        'https://news.google.com/search?q=oneplus&hl=en-IN&gl=IN&ceid=IN%3Aen',
        'https://news.google.com/search?q=samsung&hl=en-IN&gl=IN&ceid=IN%3Aen',
        'https://news.google.com/search?q=moto&hl=en-IN&gl=IN&ceid=IN%3Aen'
    ]

    def scroll(self, driver, timeout):
        scroll_pause_time = timeout

        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
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

    def format_url(self, url):
        newURL = url.replace(".", "https://news.google.com")
        return newURL
    
    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.google.com",
            wait_time=5,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        driver.maximize_window()
        for keyword in self.keywords:
            # driver.find_element_by_xpath("(//input)[2]").clear()
            driver.get(keyword)
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "(//input)[2]")))
            time.sleep(4)
            # search_input = driver.find_element_by_xpath("(//input)[2]")
            # search_input.send_keys(keyword)
            # search_input.send_keys(Keys.ENTER)
            # time.sleep(4)

            self.scroll(driver, 3)

            html1 = driver.page_source
            response1 = Selector(text=html1)
            
            articles = response1.xpath("//main//article//h3")
            
            for article in articles:
                yield{
                    'Keyword': keyword,
                    'Article': article.xpath("normalize-space(.//a/text())").get(),
                    'Link': self.format_url(article.xpath(".//a/@href").get())
                }
