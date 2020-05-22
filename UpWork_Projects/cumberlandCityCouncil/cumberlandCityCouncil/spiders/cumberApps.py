# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector
import time
import datetime


class CumberappsSpider(scrapy.Spider):
    name = 'cumberApps'
    urls = [
        'https://cumberland-eplanning.t1cloud.com/Pages/XC.Track/SearchApplication.aspx?d=thismonth&k=LodgementDate&',
        'https://cumberland-eplanning.t1cloud.com/Pages/XC.Track/SearchApplication.aspx?d=thismonth&k=DeterminationDate&'
    ]

    def convert_dateTime(self, value):
        try:
            date_time_obj = datetime.datetime.strptime(value, '%d/%m/%Y')
            return date_time_obj.date()
        except:
            return None

    def remove_nonUTF_char(self, value):
        try:
            filter1 = value.replace('\n', ' ').replace('\r', '')
            return bytes(filter1, 'utf-8').decode('utf-8','ignore')
        except:
            return None

    def gen_app_url(self, rel_url):
        try:
            return f"https://cumberland-eplanning.t1cloud.com/{rel_url.strip('../..')}"
        except:
            return None

    def get_applicants(self, applicant_list):
        app_list = []
        try:
            for applicant in applicant_list:
                if applicant.startswith("Applicant"):
                    x1 = applicant.replace('Applicant: ','')
                    app_list.append(self.remove_nonUTF_char(x1))
            return app_list
        except:
            return None

    def start_requests(self):
        yield SeleniumRequest(
            url=self.urls[0],
            wait_time=8,
            callback=self.app_listings
        )

    def app_listings(self, response):
        driver = response.meta['driver']
        cntr = True
        while cntr:
            time.sleep(3)
            html = driver.page_source
            response = Selector(text=html)

            app_listings = response.xpath("//div[@id='searchresult']/div[@class='result']")
            for apps in app_listings:
                url = self.gen_app_url(apps.xpath(".//a[@class='search']/@href").get())
                applicant = apps.xpath(".//div/text()").getall()
                yield scrapy.Request(
                    url=url,
                    callback=self.parse,
                    meta={
                        'applicant': applicant
                    }
                )

            next_page = response.xpath("//a[@class='next']")
            if next_page:
                np = driver.find_element_by_xpath("//a[@class='next']")
                np.click()
            else:
                cntr = False

        for url in self.urls[1:]:
            yield SeleniumRequest(
                url=url,
                wait_time=8,
                callback=self.app_listings
            )

    def parse(self, response):
        yield{            
            'appNum': self.remove_nonUTF_char(response.xpath("normalize-space(//h2/text())").get()),
            'nameLGA': 'Cumberland',
            'codeLGA': '12380',
            'address': self.remove_nonUTF_char(response.xpath("normalize-space(//div[@class='applicationInfoDetail']/a/text())").get()),
            'activity': self.remove_nonUTF_char(response.xpath("normalize-space(//div[text()='Description:']/following-sibling::div/text())").get()),
            'applicant': self.get_applicants(response.request.meta['applicant']),
            'lodgeDate': self.convert_dateTime(response.xpath("normalize-space(//div[text()='Lodged date:']/following-sibling::div/text())").get()),
            'decisionDate': self.convert_dateTime(response.xpath("normalize-space(//div[text()='Decision date:']/following-sibling::div/text())").get()),
            'status': self.remove_nonUTF_char(response.xpath("normalize-space(//div[text()='Decision:']/following-sibling::div/text())").get()),
            'url' : response.url            
        }