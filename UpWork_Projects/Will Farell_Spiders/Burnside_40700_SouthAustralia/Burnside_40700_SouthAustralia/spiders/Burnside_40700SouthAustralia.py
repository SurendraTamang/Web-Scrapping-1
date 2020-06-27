# -*- coding: utf-8 -*-
import scrapy
import time
import datetime
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class Burnside40700southaustraliaSpider(scrapy.Spider):
    name = 'Burnside_40700SouthAustralia'

    urls = [
        "https://eservices.burnside.sa.gov.au/eProperty/P1/eTrack/eTrackApplicationSearchResults.aspx?Field=D&Period=TM&r=P1.WEBGUEST&f=%24P1.ETR.SEARCH.DTM",
        "https://eservices.burnside.sa.gov.au/eProperty/P1/eTrack/eTrackApplicationSearchResults.aspx?Field=S&Period=TM&r=P1.WEBGUEST&f=%24P1.ETR.SEARCH.STM"
    ]

    def format_dateTime(self, value):
        try:
            return datetime.datetime.strptime(str(value), '%d/%m/%Y').date()
        except:
            return None

    def format_text(self, value):
        result = ",".join(i.strip() for i in value)
        return result

    def gen_url(self, value):
        li = value.split("\\")
        return "%5c".join(i for i in li)

    def start_requests(self):
        yield SeleniumRequest(
            url="https://eservices.burnside.sa.gov.au",
            wait_time=5,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        driver.maximize_window()

        for url in self.urls:
            cntr = 1
            driver.get(url)
            WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "(//tbody/tr[@class='normalRow' or @class='alternateRow'])[1]//td[1]/a")))
            
            while True:
                html = driver.page_source
                resp_obj = Selector(text=html)

                listings = resp_obj.xpath("//tbody/tr[@class='normalRow' or @class='alternateRow']")
                for lists in listings:
                    app_num = lists.xpath("normalize-space(.//td[1]/a/text())").get()
                    yield{
                        'appNum': app_num,
                        'nameLGA': 'Burnside',
                        'codeLGA': '40700',
                        'address': lists.xpath("normalize-space(.//td[5]/a/text())").get(),
                        'activity': lists.xpath("normalize-space(.//td[3]/text())").get(),
                        'applicant': self.format_text(lists.xpath(".//td[6]/text()").getall()),
                        'lodgeDate': self.format_dateTime(lists.xpath("normalize-space(.//td[2]/text())").get()),
                        'decisionDate': None,
                        'status': None,
                        'url': f'''https://eservices.burnside.sa.gov.au/eProperty/P1/eTrack/eTrackApplicationDetails.aspx?r=P1.WEBGUEST&f=%24P1.ETR.APPDET.VIW&ApplicationId={self.gen_url(app_num)}'''
                    }
                cntr += 1
                next_page = resp_obj.xpath(f"//a[text()={cntr}]")
                if next_page:
                    driver.find_element_by_xpath(f"//a[text()={cntr}]").click()
                    time.sleep(6)
                else:
                    break

