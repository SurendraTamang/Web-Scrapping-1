import scrapy
from scrapy_selenium import SeleniumRequest

# from ..utils import cookie_parser


class DnbspiderSpider(scrapy.Spider):
    name = 'dnbSpider'

    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.tiffany.com/jewelry/necklaces-pendants/tiffany-t-diamond-and-mother-of-pearl-circle-pendant-64026828/",
            wait_time=20,
            callback=self.parse
        )

    # def start_requests(self):
    #     yield scrapy.Request(
    #         # url="https://www.dnb.com/business-directory.html",
    #         url="https://www.dnb.com/business-directory/company-information.education-sector.us.html?page=1",
    #         cookies=cookie_parser(),
    #         callback=self.parse
    #     )

    # def getSubCategory(self, response):
    #     subCategories = response.xpath("//div[contains(@class, 'accordion_list')]/div")
    #     for subCategory in subCategories:
    #         yield scrapy.Request(
    #             url=f'''https://www.dnb.com{subCategory.xpath(".//div[contains(@class, 'link')]/a/@href").get()}''',
    #             callback=self.getCountry,
    #             meta={
    #                 'category': subCategory.xpath("normalize-space(.//div[@class='title']/text())").get(),
    #                 'subCategory': subCategory.xpath("normalize-space(.//div[contains(@class, 'link')]/a/text())").get()
    #             }
    #         )

    # def getCountry(self, response):
    #     yield scrapy.Request(
    #         url="",
    #         callback=self.parse
    #     )

    def parse(self, response):
        driver = response.meta['driver']
        html = driver.page_source
        print(html)
        yield{
            'url': response.url,
            # 'category': response.request.meta('category'),
            # 'category': response.request.meta('subCategory')
        }
