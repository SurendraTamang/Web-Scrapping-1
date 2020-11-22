import scrapy


class Test1Spider(scrapy.Spider):
    name = 'test1'
    
    def start_requests(self):
        yield scrapy.Request(
            url="https://www.autoscout24.com/offers/audi-a6-2-5tdi-diesel-silver-70243834-5820-4a85-9d1f-6062ab9871c6?cldtidx=2&cldtsrc=listPage",
            callback=self.parse
        )

    def parse(self, response):
        yield{
            'Make Model': response.xpath("normalize-space(//span[contains(@class, 'makemodel')]/text())").get(),
            'Version': response.xpath("normalize-space(//span[contains(@class, 'version')]/text())").get(),
            'Price': response.xpath("normalize-space(//div[contains(@class, 'price')]/h2//text())").get()
        }