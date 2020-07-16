import scrapy
from scrapy import Selector
from scrapy_selenium import SeleniumRequest


class VicbarspiderSpider(scrapy.Spider):
    name = 'vicbarSpider'
    
    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.vicbar.com.au/find-barrister",
            wait_time=5,
            callback=self.parse
        )

    def parse(self, response):
        listings = response.xpath("(//div[@class='view-content'])[2]/div")
        for lists in listings:
            yield{
                'name': lists.xpath("normalize-space(.//div[contains(@class, 'full-name')]/div/div/text())").get(),
                'eamil': lists.xpath("normalize-space(.//div[contains(@class, 'user-email')]//span/text())").get(),
                'phone': lists.xpath("normalize-space(.//div[contains(@class, 'internal-phone')]/div/div/text())").get(),
                'chambers': lists.xpath("normalize-space(.//div[@class='field-chambers']/a/text())").get(),
                'url': f'''https://www.vicbar.com.au{lists.xpath(".//a[@class='pre_render_alter']/@href").get()}'''
            }
