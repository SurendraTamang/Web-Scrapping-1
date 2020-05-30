# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
import time
import datetime


class WhitehorsespiderSpider(scrapy.Spider):
    name = 'whitehorseSpider'

    def remove_nexLine_char(self, value):
        try:
            filter1 = value.replace('\n', ' ').replace('\r', '')
            return filter1
            #return bytes(filter1, 'utf-8').decode('utf-8','ignore')
        except:
            return None
    
    def start_requests(self):
        yield SeleniumRequest(
            url="https://eservices.whitehorse.vic.gov.au/ePathway/Production/Web/default.aspx",
            wait_time=6,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        driver.find_element_by_xpath("//b[text()='online enquiry tool']").click()
        driver.switch_to.window(driver.window_handles[1])
        driver.find_element_by_xpath("//td[text()='Planning Register']/preceding-sibling::td/input").click()
        driver.find_element_by_xpath("//input[contains(@value, 'Next')]").click()
        time.sleep(5)
        driver.find_element_by_xpath("//a[text()='Date Search']").click()
        driver.find_element_by_xpath("//input[contains(@value, 'Search')]").click()
        time.sleep(5)

        while True:
            html = driver.page_source
            response_obj = Selector(text=html)
            app_list = response_obj.xpath("//tbody//div[@class='ContentText' or 'AlternateContentText']/a")
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[2])
            for app in app_list:
                url = f'https://eservices.whitehorse.vic.gov.au/ePathway/Production/Web/GeneralEnquiry/{app.xpath(".//@href").get()}'                
                driver.get(url)
                html1 = driver.page_source
                response_obj1 = Selector(text=html1)
                lDate = response_obj1.xpath("normalize-space(//span[text()='Application Date']/following-sibling::div/text())").get()
                try:
                    if lDate:
                        lodgeDate = datetime.datetime.strptime(str(lDate), '%d/%m/%Y').date()
                    else:
                        lodgeDate = None
                except:
                    lodgeDate = None
                yield{
                    'appNum': response_obj1.xpath("normalize-space(//span[text()='Application Number']/following-sibling::div/text())").get(),
                    'nameLGA': 'Whitehorse',
                    'codeLGA': '26980',
                    'address': response_obj1.xpath("normalize-space(//span[text()='Application Location']/following-sibling::div/text())").get(),
                    'activity': self.remove_nexLine_char(response_obj1.xpath("//span[text()='Description']/following-sibling::span/text()").get()),
                    'applicant': None,
                    'lodgeDate': lodgeDate,
                    'decisionDate': None,
                    'status': response_obj1.xpath("normalize-space(//span[text()='Status']/following-sibling::div/text())").get(),
                    'url' : url
                }
            driver.close()
            driver.switch_to.window(driver.window_handles[1])
            next_page = response_obj.xpath("//td[@id='ctl00_MainBodyContent_mPagingControl_TableCell5']/input[@type='image']")
            if next_page:
                driver.find_element_by_xpath("//td[@id='ctl00_MainBodyContent_mPagingControl_TableCell5']/input[@type='image']").click()
                time.sleep(7)
            else:
                break