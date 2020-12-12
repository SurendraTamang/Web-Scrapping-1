import scrapy


class PartdetailsSpider(scrapy.Spider):
    name = 'partDetails'
    allowed_domains = ['custom.partref.com']
    start_urls = ['http://custom.partref.com/']

    def parse(self, response):
        pass
