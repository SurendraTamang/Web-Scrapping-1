import scrapy
import pandas as pd


class TestspiderSpider(scrapy.Spider):
    name = 'testSpider'

    df = pd.read_excel("D:/linodeWorkspace/ocado/ocadoProducts.xlsx", sheet_name='final')

    def start_requests(self):
        for _, value in self.df.iterrows():
            yield scrapy.Request(
                url=value['url'],
                callback=self.parse,
                dont_filter=True,
                meta={
                    'url': value['url']
                }
            )

    def parse(self, response):
        sSize = response.xpath("normalize-space(//tbody/tr/th[2]/text())").get()
        if sSize == "" or sSize == None:
            sSize = response.xpath("normalize-space(//th[contains(text(), 'Values')]/following-sibling::th/text())").get()
        yield{
            'cal per quantity': sSize,
            'Lvl1Cat': response.xpath("normalize-space(//ul[contains(@class, 'categories')]/li[2]/a/text())").get(),
            'Lvl2Cat': response.xpath("normalize-space(//ul[contains(@class, 'categories')]/li[3]/a/text())").get(),
            'Lvl3Cat': response.xpath("normalize-space(//ul[contains(@class, 'categories')]/li[4]/a/text())").get(),
            'url': response.request.meta['url']
        }
