# -*- coding: utf-8 -*-
import scrapy
import time
import re
from datetime import date, timedelta, datetime
from scrapy import Selector
from selenium.webdriver.common.action_chains import ActionChains
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class InwestSpiderSpider(scrapy.Spider):
    name = 'inWest_spider'

    def last_thirtyDays_check(self, value):
        current_date = date.today().isoformat()   
        thirty_days_back = (date.today()-timedelta(days=30)).isoformat()
        current_date_fmt = datetime.strptime(current_date, '%Y-%m-%d').date()
        thirty_days_back_fmt = datetime.strptime(thirty_days_back, '%Y-%m-%d').date()
        try:
            if value >= thirty_days_back_fmt and value <= current_date_fmt:
                return True
        except:
            return False

    def convert_dateTime(self, value):
        try:
            if value == "<span></span>":
                return None
            else:
                pattern = "<span>(.*?)</span>"
                substring = re.search(pattern, value).group(1)
                try:
                    date_time_obj = datetime.strptime(substring, '%d-%B-%Y %H:%M:%S')
                    return date_time_obj.date()
                except:
                    date_time_obj = datetime.strptime(substring, '%d-%b-%Y %H:%M:%S')
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
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "(//a[@class='hyperlink'])[3]"))).click()
        # driver.implicitly_wait(15)
        # time.sleep(7)
        # driver.find_element_by_xpath("(//a[@class='hyperlink'])[3]").click()
        WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//span[@class='resultsRange']")))
        
        #Fetching the total number of listings.
        html_init = driver.page_source
        response_init = Selector(text=html_init)
        t_count_str = response_init.xpath("//span[@class='resultsRange']/text()").get()
        li = [re.findall(r'\d+', t_count_str )]
        total_cnt = int(''.join(i for i in li[0]))
        no_of_scrolls = total_cnt//40
        if no_of_scrolls >= 20:
            no_of_scrolls = 5
        else:
            pass
        
        # Scrolling through the listings.
        for i in range(1,no_of_scrolls+1):
            # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"(//div[contains(@class, 'headingField')]/child::div/span)[{i*40}]"))).click()
            element = driver.find_element_by_xpath(f"(//div[contains(@class, 'headingField')]/child::div/span)[{i*40}]")
            driver.execute_script("arguments[0].click();", element)
            time.sleep(8)

        # Scrapping the data.
        driver.implicitly_wait(5)
        html = driver.page_source
        response_obj = Selector(text=html)
        listings = response_obj.xpath("//div[@class='thumbnailItemsContainer']/div[contains(@class, 'thumbnailItem')]")
        for lists in listings:
            lDate = self.convert_dateTime(lists.xpath(f".//div[contains(@class, 'mainSection')]/div[4]//label[@title='Lodged']/parent::div/following-sibling::div/span").get())
            if self.last_thirtyDays_check(lDate):
                yield{
                    'appNum': lists.xpath(f"normalize-space(.//div[contains(@class, 'headingField')]/child::div/span/text())").get(),
                    'nameLGA': 'Inner West',
                    'codeLGA': '14170',
                    'address': lists.xpath(f"normalize-space(.//div[contains(@class, 'headingField')]/following-sibling::div/div/span/text())").get(),
                    'activity': lists.xpath(f"normalize-space(.//div[contains(@class, 'mainSection')]/div[3]//div[contains(@class, 'thbFld_Description')]/div/span/text())").get(),
                    'applicant': None,
                    'lodgeDate': lDate,
                    'decisionDate': self.convert_dateTime(lists.xpath(f".//div[contains(@class, 'mainSection')]/div[4]//label[@title='Accepted']/parent::div/following-sibling::div/span").get()),
                    'status': lists.xpath(f"normalize-space(.//div[@class='thumbnailSection nonStacked  hasOnlyDataFields']//div[contains(@class, 'lastVisibleField')]/div/span/text())").get(),
                    'url' : None
                }