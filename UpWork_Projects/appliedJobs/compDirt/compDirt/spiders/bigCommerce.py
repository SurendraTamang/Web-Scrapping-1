import scrapy


class BigcommerceSpider(scrapy.Spider):
    name = 'bigCommerce'

    def start_requests(self):
        yield scrapy.Request(
            url="https://partners.bigcommerce.com/directory/search?f0=Expertise&f0v0=Web+Developer",
            callback=self.parse
        )

    def parse(self, response):
        cards = response.xpath("//div[@id='partnerCards']/div")
        for card in cards:
            yield scrapy.Request(
                url=f'''https://partners.bigcommerce.com{response.xpath(".//h3/a/@href").get()}''',
                callback=self.compDetails,
                meta={
                    'Company Name': response.xpath("normalize-space(.//h3/a/text())").get()
                }
            )
        
        next_page = response.xpath("//a[text()='Next']/@href").get()
        if next_page:
            yield scrapy.Request(
                url=f"https://partners.bigcommerce.com{next_page}",
                callback=self.parse
            )
        
    def compDetails(self, response):
        yield {
            'Company Name': response.request.meta['Company Name'],
            'Company Webiste': response.xpath("//p[text()='Website:']/following-sibling::p/a/@href").get(),
            'Source Website': response.url
        }
