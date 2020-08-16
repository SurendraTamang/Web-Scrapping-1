import scrapy
import pandas as pd


class AldinewSpider(scrapy.Spider):
    name = 'aldiNew'

    df = pd.read_excel("D:/linodeWorkspace/Finished/aldi/aldiProducts.xlsx")

    def start_requests(self):
        for _, value in self.df.iterrows():
            yield scrapy.Request(
                url=value['Product (link)'],
                callback=self.parse,
                dont_filter=True,
                meta={
                    'url': value['Product (link)']
                }
            )

    def parse(self, response):
        prodName = response.xpath("normalize-space(//h1[@class='product-details__name']/text())").get()
        brandName = response.xpath("normalize-space(//p[contains(text(), 'Brand')]/following-sibling::p/text())").get()
        if brandName == "" or brandName == None:
            newName = prodName
        else:
            newName = f"{brandName} {prodName}"
        yield{
            'url': response.request.meta['url'],
            'name': newName
        }
