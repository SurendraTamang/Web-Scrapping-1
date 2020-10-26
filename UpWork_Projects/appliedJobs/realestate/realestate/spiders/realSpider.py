import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy import Selector
import time


class RealspiderSpider(scrapy.Spider):
    name = 'realSpider'

    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.realestate.com.au/buy",
            wait_time=5,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        time.sleep(30)
        
        while True:
            html1 = driver.page_source
            response1 = Selector(text=html1)

            ads = response1.xpath("//div/article")
            for ad in ads:
                yield{
                    'Property URL': f'''https://www.realestate.com.au{ad.xpath(".//a[@class='details-link ']/@href").get()}''',
                    'Property Image': ad.xpath(".//img[contains(@class, 'property')]/@src").get(),
                    'Address': ad.xpath("normalize-space(.//h2/a/span/text())").get(),
                    'Beds': ad.xpath("normalize-space(.//span[contains(@class, 'beds')]/text()[2])").get(),
                    'Baths': ad.xpath("normalize-space(.//span[contains(@class, 'baths')]/text()[2])").get(),
                    'Cars': ad.xpath("normalize-space(.//span[contains(@class, 'cars')]/text()[2])").get(),
                    'Size': ad.xpath("normalize-space(.//span[contains(@class, 'size')]/text()[2])").get()
                }
            next_page = response1.xpath("//a[@rel='next']/@href").get()
            if next_page:
                driver.get(next_page)
                time.sleep(6)
