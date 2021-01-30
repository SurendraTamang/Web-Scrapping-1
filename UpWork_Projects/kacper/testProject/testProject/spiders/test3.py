import scrapy


class Test3Spider(scrapy.Spider):
    name = 'test3'
    
    def start_requests(self):
        yield scrapy.Request(
            url="https://www.realtor.com/realestateandhomes-search/Georgia/pg-2",
            callback=self.parse
        )

    def parse(self, response):
        print(response.xpath("//ul[@data-testid='property-list-container']/li"))
