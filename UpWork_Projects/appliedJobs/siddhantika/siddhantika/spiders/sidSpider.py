import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy import Selector
import time

class SidspiderSpider(scrapy.Spider):
    name = 'sidSpider'
    
    urls = [
        # 'http://www.siddhantika.com/ephemeris/venus-sign-table',
        # 'http://www.siddhantika.com/ephemeris/sun-sign-table',
        'http://www.siddhantika.com/ephemeris/2013'
    ]

    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.google.com",
            wait_time=5,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        for url in self.urls:
            driver.get(url)
            time.sleep(3)
            html = driver.page_source
            response1 = Selector(text=html)
            rows = response1.xpath("(//table/tbody)[3]//td[@valign='top']/parent::tr")
            for row in rows:
                event = row.xpath("normalize-space(.//td[@valign='top'][3]/text())").get()
                li = event.split(" ")
                if li[1] == "enters":
                    yield{
                        'Date': row.xpath("normalize-space(.//td[@valign='top'][1]/text())").get(),
                        'Time': row.xpath("normalize-space(.//td[@valign='top'][2]/text())").get(),
                        'Planet': li[0],
                        'Star Sign': li[2]
                    }
