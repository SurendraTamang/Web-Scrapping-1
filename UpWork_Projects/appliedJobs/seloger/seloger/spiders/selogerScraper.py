import scrapy


class SelogerscraperSpider(scrapy.Spider):
    name = 'selogerScraper'
    
    def start_requests(self):
        yield scrapy.Request(
            # url="https://www.seloger.com/list.htm?projects=2%2C5&types=2%2C1&natures=1%2C2%2C4&places=%5B%7Bdiv%3A2238%7D%5D&enterprise=0&qsVersion=1.0&LISTING-LISTpg=1",
            url="https://www.seloger.com/annonces/achat/appartement/boulogne-billancourt-92/grenier-point-du-jour/162807961.htm?projects=2,5&types=2,1&natures=1,2,4&places=[{div:2238}]&enterprise=0&qsVersion=1.0&m=search_to_detail",
            callback=self.parse
        )

    def parse(self, response):
        # listings = response.xpath("//div[contains(@class, 'block__ShadowedBlock-sc')]")
        pieces = response.xpath("//div[contains(text(), 'pièces')]/text()").get()
        print(pieces)
