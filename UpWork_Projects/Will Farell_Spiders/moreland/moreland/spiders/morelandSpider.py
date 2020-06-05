# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
import time
from datetime import date, timedelta, datetime


class MorelandspiderSpider(scrapy.Spider):
    name = 'morelandSpider'

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

    def format_dateTime(self, value):
        try:
            return datetime.strptime(str(value), '%d/%m/%Y').date()
        except:
            return None

    def remove_nexLine_char(self, value):
        try:
            filter1 = value.replace('\n', ' ').replace('\r', '')
            return filter1
        except:
            return None

    def start_requests(self):
        yield SeleniumRequest(
            url="https://eservices.moreland.vic.gov.au/ePathway/Production/Web/GeneralEnquiry/EnquiryLists.aspx?ModuleCode=LAP&js=-1768304710",
            wait_time=5,
            callback=self.parse
        )

    def parse(self, response):
        categories = [
            'Planning permit applications in progress',
            'Subdivision certifications in progress'
        ]
        driver = response.meta['driver']
        driver.maximize_window()
        for category in categories:            
            driver.find_element_by_xpath(f"//td[text()='{category}']/preceding-sibling::td/input").click()
            time.sleep(5)
            driver.find_element_by_xpath("//input[@value='Next']").click()

            while True:
                cntr = 0
                html = driver.page_source
                response_obj = Selector(text=html)
                app_list = response_obj.xpath("//table[@class='ContentPanel']/tbody//tr[@class='ContentPanel' or 'AlternateContentPanel' and @class!='ContentPanelHeading']")
                
                for app in app_list:
                    lDate = self.format_dateTime(app.xpath("normalize-space(.//td[2]/span/text())").get())
                    if self.last_thirtyDays_check(lDate):
                        cntr += 1
                        yield{
                            'appNum': app.xpath("normalize-space(.//td[1]/a/text())").get(),
                            'nameLGA': 'Moreland',
                            'codeLGA': '25250',
                            'address': app.xpath("normalize-space(.//td[4]/span/text())").get(),
                            'activity': self.remove_nexLine_char(app.xpath(".//td[3]/span/text()").get()),
                            'applicant': None,
                            'lodgeDate': lDate,
                            'decisionDate': None,
                            'status': app.xpath("normalize-space(.//td[5]/span/text())").get(),
                            'url' : f'''https://eservices.moreland.vic.gov.au/ePathway/Production/Web/GeneralEnquiry/{app.xpath(".//td[1]/a/@href").get()}'''
                        }
                    else:
                        pass
                next_page = response_obj.xpath("//td[@id='ctl00_MainBodyContent_mPagingControl_TableCell5']/input[@type='image']")
                if next_page and cntr != 0:
                    driver.find_element_by_xpath("//td[@id='ctl00_MainBodyContent_mPagingControl_TableCell5']/input[@type='image']").click()
                    time.sleep(5)
                else:
                    break   

            driver.get("https://eservices.moreland.vic.gov.au/ePathway/Production/Web/GeneralEnquiry/EnquiryLists.aspx?ModuleCode=LAP&js=-1768304710")     