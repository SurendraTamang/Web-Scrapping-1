# -*- coding: utf-8 -*-
import scrapy
import time
import re
import datetime
from scrapy import Selector
from selenium.webdriver.common.action_chains import ActionChains
from scrapy_selenium import SeleniumRequest


class InwestSpiderSpider(scrapy.Spider):
    name = 'inWest_spider'

    def convert_dateTime(self, value):
        try:
            if value == "<span></span>":
                return None
            else:
                pattern = "<span>(.*?)</span>"
                substring = re.search(pattern, value).group(1)
                try:
                    date_time_obj = datetime.datetime.strptime(substring, '%d-%B-%Y %H:%M:%S')
                    return date_time_obj.date()
                except:
                    date_time_obj = datetime.datetime.strptime(substring, '%d-%b-%Y %H:%M:%S')
                    return date_time_obj.date()
        except:
            return None
    
    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.innerwest.nsw.gov.au/about/get-in-touch/online-self-service",
            wait_time=6,
            callback=self.parse
        )

    def parse(self, response):
        # Accepting T&C and navigating to App listing page
        driver = response.meta['driver']
        driver.maximize_window()
        driver.find_element_by_xpath("//a[text()='Enter as a guest']").click()
        time.sleep(7)
        driver.find_element_by_xpath("(//a[@class='hyperlink'])[3]").click()
        time.sleep(15)
        
        # Fetching the total number of listings.
        html_init = driver.page_source
        response_init = Selector(text=html_init)
        t_count_str = response_init.xpath("//span[@class='resultsRange']/text()").get()
        li = [re.findall(r'\d+', t_count_str )]
        total_cnt = int(''.join(i for i in li[0]))
        no_of_scrolls = total_cnt//40
        
        # Scrolling through the listings.
        for i in range(1,no_of_scrolls+1):
            element = driver.find_element_by_xpath(f"(//div[contains(@class, 'headingField')]/child::div/span)[{i*40}]")
            driver.execute_script("arguments[0].click();", element)
            time.sleep(8)

        # Scrapping the data.
        time.sleep(5)
        html = driver.page_source
        response_obj = Selector(text=html)
        listings = response_obj.xpath("//div[@class='thumbnailItemsContainer']/div[contains(@class, 'thumbnailItem')]")
        for lists in listings:
            yield{
                'appNum': lists.xpath(f"normalize-space(.//div[contains(@class, 'headingField')]/child::div/span/text())").get(),
                'nameLGA': 'InnerWest',
                'codeLGA': '14170',
                'address': lists.xpath(f"normalize-space(.//div[contains(@class, 'headingField')]/following-sibling::div/div/span/text())").get(),
                'activity': lists.xpath(f"normalize-space(.//div[contains(@class, 'mainSection')]/div[3]//div[contains(@class, 'thbFld_Description')]/div/span/text())").get(),
                'applicant': None,
                'lodgeDate': self.convert_dateTime(lists.xpath(f".//div[contains(@class, 'mainSection')]/div[4]//label[@title='Lodged']/parent::div/following-sibling::div/span").get()),
                'decisionDate': self.convert_dateTime(lists.xpath(f".//div[contains(@class, 'mainSection')]/div[4]//label[@title='Accepted']/parent::div/following-sibling::div/span").get()),
                'status': lists.xpath(f"normalize-space(.//div[@class='thumbnailSection nonStacked  hasOnlyDataFields']//div[contains(@class, 'lastVisibleField')]/div/span/text())").get(),
                'url' : None
            }