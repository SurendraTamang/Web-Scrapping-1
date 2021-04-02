import scrapy
import pandas as pd


class BivurlsSpider(scrapy.Spider):
    name = 'bivUrls'

    df = pd.read_excel("postcode.xlsx")
    urlsLi = []
    
    def start_requests(self):
        for _,val in self.df.iterrows():
            yield scrapy.Request(
                url=f"https://www.biv.be/de-vastgoedmakelaar/alle-vastgoedmakelaars-vind-je-hier?keys=&location={val['code']}&city=",
                callback=self.parse
            )

    def parse(self, response):
        searchRes = response.xpath('//div[@class="search-results-list"]//ol/li')
        for res in searchRes:
            url = res.xpath(".//a/@href").get()
            if url not in self.urlsLi:
                self.urlsLi.append(url)
                yield{
                    'Url': url
                }

        nextPage = response.xpath("//li[@class='pager-next']/a/@href").get()
        if nextPage:
            yield scrapy.Request(
                url=nextPage,
                callback=self.parse
            )