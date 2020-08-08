import scrapy
import pandas as pd


class TestSpider(scrapy.Spider):
    name = 'test'

    df = pd.read_excel("D:/linodeWorkspace/morrisons/links.xlsx")
    
    def start_requests(self):
        for _, value in self.df.iterrows():
            yield scrapy.Request(
                url=value['url'],
                callback=self.parse,
                dont_filter=True
            )

    def parse(self, response):
        yield {
            'productName': response.xpath("normalize-space(//header[@class='bop-title']/h2/text())").get(),
            'quantity': response.xpath("normalize-space(//header[@class='bop-title']/h2/span/text())").get(),
            'price': response.xpath("normalize-space(//h2[contains(@class, 'bop-price__current')]/text())").get(),
            'img_url': f'''https://groceries.morrisons.com{response.xpath("//img[@role='presentation']/@src").get()}''',
            'url': response.url,
            'cal1': response.xpath("//table/tbody/tr[2]/td[1]/text()").get(),
            'cal2': response.xpath("//table/tbody/tr[2]/td[2]/text()").get(),
            'cal3': response.xpath("//table/tbody/tr[2]/td[3]/text()").get()
        }
