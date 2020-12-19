import scrapy


class IdeaurlgenSpider(scrapy.Spider):
    name = 'ideaUrlGen'
    
    def start_requests(self):
        yield scrapy.Request(
            url="https://www.idealista.com",
            callback=self.getPropTypeUrl
        )

    def getPropTypeUrl(self, response):
        propTypeUrls = response.xpath("//div[@class='third-level-menu'][1]/ul/li/a/@href").getall()
        for propTypeUrl in propTypeUrls:
            yield scrapy.Request(
                url=f"https://www.idealista.com{propTypeUrl}",
                callback=self.getProvinceUrls
            )
    
    def getProvinceUrls(self, response):
        provUrls = response.xpath("//div[contains(@class, 'locations-list')]/ul/li/a/@href").getall()
        for provUrl in provUrls:
            yield scrapy.Request(
                url=f"https://www.idealista.com{provUrl}",
                callback=self.parse
            )
    def parse(self, response):
        yield{
            'Province Url': None,
            'District Url': None,
        }
