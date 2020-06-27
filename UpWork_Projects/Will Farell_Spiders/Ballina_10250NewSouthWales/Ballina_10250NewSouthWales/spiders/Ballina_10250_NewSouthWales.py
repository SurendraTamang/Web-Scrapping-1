# -*- coding: utf-8 -*-
import scrapy
import time
import datetime
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class Ballina10250NewsouthwalesSpider(scrapy.Spider):
    name = 'Ballina_10250_NewSouthWales'

    urls = [
        "http://da.ballina.nsw.gov.au/Application/AdvancedSearchResult?DateFrom=1%2f06%2f2020&DateTo=25%2f06%2f2020&DateType=1&RemoveUndeterminedApplications=False&ApplicationType=&ShowOutstandingApplications=False&ShowExhibitedApplications=False&IncludeDocuments=False",
        "http://da.ballina.nsw.gov.au/Application/AdvancedSearchResult?DateFrom=1%2f06%2f2020&DateTo=25%2f06%2f2020&DateType=2&RemoveUndeterminedApplications=True&ApplicationType=&ShowOutstandingApplications=False&ShowExhibitedApplications=False&IncludeDocuments=False"
    ]

    def format_dateTime(self, value):
        try:
            return datetime.datetime.strptime(str(value), '%d/%m/%Y').date()
        except:
            return None

    def format_text(self,value):
        try:
            if "(" in value:
                li = value.split("(")
                return li[0].strip()
            else:
                li = value.split(":")
                return li[1].strip()
        except:
            return value
    
    def start_requests(self):
        yield SeleniumRequest(
            url="http://da.ballina.nsw.gov.au/Home/Disclaimer",
            wait_time=5,
            callback=self.app_listings
        )

    def app_listings(self, response):
        driver = response.meta['driver']
        driver.maximize_window()
        
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Agree']"))).click()
        time.sleep(5)

        for url in self.urls:
            cntr = 1
            driver.get(url)
            # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//select[@name='applicationsTable_length']"))).click()
            # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//option[@value='100']"))).click()
            time.sleep(10)

            while True:
                cntr += 1
                html_init = driver.page_source
                resp_obj_init = Selector(text=html_init)

                listings = resp_obj_init.xpath("//tbody/tr[@role='row']")
                driver.execute_script("window.open('');")                
                driver.switch_to.window(driver.window_handles[1])
                for lists in listings:
                    url = f'''http://da.ballina.nsw.gov.au/Application/{lists.xpath(".//td/a[text()='Details']/@href").get()}'''
                    driver.get(url)
                    # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Show All']"))).click()
                    html = driver.page_source
                    resp_obj = Selector(text=html)
                    yield{
                        'appNum': lists.xpath("normalize-space(.//td[2]/text())").get(),
                        'nameLGA': 'Ballina',
                        'codeLGA': '10250',
                        'address': self.format_text(resp_obj.xpath("normalize-space(//td[@id='property-list']/text())").get()),
                        'activity': resp_obj.xpath("normalize-space(//td[@id='description']/text())").get(),
                        'applicant': self.format_text(resp_obj.xpath("normalize-space(//td[contains(text(), 'Applicant')]/text())").get()),
                        'lodgeDate': self.format_dateTime(lists.xpath("normalize-space(.//td[4]/text())").get()),
                        'decisionDate': None,
                        'status': self.format_text(resp_obj.xpath("normalize-space(//a[text()='Decision']/parent::h3/following-sibling::div[1]/table/tbody/tr/td)").get()),
                        'url': url
                    }
                driver.close()  
                driver.switch_to.window(driver.window_handles[0])
                next_page = resp_obj_init.xpath(f"//li[@class='paginate_button ']/a[text()={cntr}]")
                if next_page:
                    driver.find_element_by_xpath(f"//li[@class='paginate_button ']/a[text()={cntr}]").click()
                    time.sleep(6)
                else:
                    break

