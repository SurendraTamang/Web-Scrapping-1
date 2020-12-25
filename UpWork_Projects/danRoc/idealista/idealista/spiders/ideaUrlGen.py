import scrapy


class IdeaurlgenSpider(scrapy.Spider):
    name = 'ideaUrlGen'
    
    def start_requests(self):
        yield scrapy.Request(
            url="https://www.idealista.com",
            callback=self.getPropTypeUrl
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
            'Province Url': response.url,
            'District Url': None,
        }
