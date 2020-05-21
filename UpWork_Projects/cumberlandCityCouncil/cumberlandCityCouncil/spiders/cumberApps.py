# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector
import time



class CumberappsSpider(scrapy.Spider):
    name = 'cumberApps'
    urls = [
        'https://cumberland-eplanning.t1cloud.com/Pages/XC.Track/SearchApplication.aspx?d=thismonth&k=LodgementDate&',
        'https://cumberland-eplanning.t1cloud.com/Pages/XC.Track/SearchApplication.aspx?d=thismonth&k=DeterminationDate&'
    ]

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
                    app_list.append(applicant.strip('Applicant: '))
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
                applicant = self.get_applicants(apps.xpath(".//div/text()").getall())
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
            'appNum': response.xpath("//h2/text()").get(),
            'nameLGA': 'Cumberland',
            'codeLGA': '12380',
            'address': response.xpath("//div[@class='applicationInfoDetail']/a/text()").getall(),
            'activity': response.xpath("//div[text()='Description:']/following-sibling::div/text()").get(),
            'applicant': response.request.meta['applicant'],
            'lodgeDate': response.xpath("//div[text()='Lodged date:']/following-sibling::div/text()").get(),
            'decisionDate': response.xpath("//div[text()='Decision date:']/following-sibling::div/text()").get(),
            'status': response.xpath("//div[text()='Decision:']/following-sibling::div/text()").get(),
            'url' : response.url
            
        }
