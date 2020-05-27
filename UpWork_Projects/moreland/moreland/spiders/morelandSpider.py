# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
import time


class MorelandspiderSpider(scrapy.Spider):
    name = 'morelandSpider'

    def remove_nexLine_char(self, value):
        try:
            filter1 = value.replace('\n', ' ').replace('\r', '')
            return filter1
            #return bytes(filter1, 'utf-8').decode('utf-8','ignore')
        except:
            return None

    def start_requests(self):
        yield SeleniumRequest(
            url="https://eservices.moreland.vic.gov.au/ePathway/Production/Web/GeneralEnquiry/EnquiryLists.aspx?ModuleCode=LAP&js=-1768304710",
            wait_time=5,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        driver.find_element_by_xpath("//td[text()='Planning permit applications in progress']/preceding-sibling::td/input").click()
        driver.find_element_by_xpath("//input[@value='Next']").click()

        while True:
            html = driver.page_source
            response_obj = Selector(text=html)
            app_list = response_obj.xpath("//table[@class='ContentPanel']/tbody//tr[@class='ContentPanel' or 'AlternateContentPanel' and @class!='ContentPanelHeading']")
            for app in app_list:
                yield{
                    'appNum': app.xpath("normalize-space(.//td[1]/a/text())").get(),
                    'nameLGA': 'Moreland',
                    'codeLGA': '25250',
                    'address': app.xpath("normalize-space(.//td[4]/span/text())").get(),
                    'activity': self.remove_nexLine_char(app.xpath(".//td[3]/span/text()").get()),
                    'applicant': None,
                    'lodgeDate': app.xpath("normalize-space(.//td[2]/span/text())").get(),
                    'decisionDate': None,
                    'status': app.xpath("normalize-space(.//td[5]/span/text())").get(),
                    'url' : f'''https://eservices.moreland.vic.gov.au/ePathway/Production/Web/GeneralEnquiry/{app.xpath(".//td[1]/a/@href").get()}'''
                }
            next_page = response_obj.xpath("//td[@id='ctl00_MainBodyContent_mPagingControl_TableCell5']/input[@type='image']")
            if next_page:
                driver.find_element_by_xpath("//td[@id='ctl00_MainBodyContent_mPagingControl_TableCell5']/input[@type='image']").click()
                time.sleep(5)
            else:
                break        