import scrapy
import pandas as pd


class IcelandnewSpider(scrapy.Spider):
    name = 'icelandNew'
    
    df = pd.read_excel("D:/linodeWorkspace/iceland/icelandProducts.xlsx", sheet_name='urls')

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
        calories = response.xpath("normalize-space(//td[contains(text(), 'Energy')]/following-sibling::td/text())").get()        
        if calories == "" or calories == None:
            calories = response.xpath("normalize-space(//td[contains(text(), 'kcal')]/text())").get()
        sSize = response.xpath("normalize-space(//tbody/tr/th[2]/text())").get()
        if sSize == "" or sSize == None:
            sSize = response.xpath("normalize-space(//th[contains(text(), 'Values')]/following-sibling::th/text())").get()
        yield{
            'url': response.request.meta['url'],
            'cal per quantity': sSize,
            'calories': calories
        }
