# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector
import time
import datetime


class ServicesSpider(scrapy.Spider):
    name = 'services'
    
    def clean_text(self, value):
        try:
            return value.strip("\xa0")
        except:
            return None

    def start_requests(self):
        yield SeleniumRequest(
            url='https://onlineservices.stirling.wa.gov.au/eProperty/P1/eTrack/eTrackApplicationSearch.aspx?r=P1.WEBGUEST&f=P1.ETR.SEARCH.ENQ',
            wait_time=5,
            callback=self.parse
        )

    def parse(self, response):
        today = datetime.date.today()
        oneMonth = datetime.timedelta(days=30)
        oneMonth = today - oneMonth

        driver = response.meta['driver']
        start_date = driver.find_element_by_xpath("//span[@id='ctl00_Content_txtDateFrom']/input")
        start_date.send_keys(str(oneMonth.strftime("%d/%m/%Y")))
        end_date = driver.find_element_by_xpath("//span[@id='ctl00_Content_txtDateTo']/input")
        end_date.send_keys(str(today.strftime("%d/%m/%Y")))
        driver.execute_script("window.scrollBy(0,1000);")
        time.sleep(6)
        submit = driver.find_element_by_xpath("//input[@value='Clear']/following-sibling::input")
        submit.click()
        time.sleep(10)
        
        html = driver.page_source
        response = Selector(text=html)

        listings = response.xpath("//table[@class='grid']/tbody")
        for listing in listings:
            yield{
                'Application_ID': self.clean_text(listing.xpath("normalize-space(.//tr[1]//div/input/@value)").get()),
                'Stage': self.clean_text(listing.xpath("normalize-space(.//tr[2]/td[2]/text())").get()),
                'Lodgement_Date': self.clean_text(listing.xpath("normalize-space(.//tr[3]/td[2]/text())").get()),
                'Description': self.clean_text(listing.xpath("normalize-space(.//tr[4]/td[2]/text())").get()),
                'Group_Description': self.clean_text(listing.xpath("normalize-space(.//tr[5]/td[2]/text())").get()),
                'Site_Address': self.clean_text(listing.xpath("normalize-space(.//tr[6]//div/input/@value)").get()),
                'Applicant_Name': self.clean_text(listing.xpath("normalize-space(.//tr[7]/td[2]/text())").get())
            }
        
