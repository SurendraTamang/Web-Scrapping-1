# -*- coding: utf-8 -*-
import scrapy


class SymbolsSpider(scrapy.Spider):
    name = 'symbols'

    def start_requests(self):
        yield scrapy.Request(
            url='http://statesymbolsusa.org',
            callback=self.listings
        )

    def listings(self, response):
        links = response.xpath("(//div[@class='item-list'])[1]/ul/li")
        for link in links:
            state_name = link.xpath("normalize-space(.//a/text())").get()
            abs_url = f'''http://statesymbolsusa.org{link.xpath(".//a/@href").get()}'''
            yield scrapy.Request(
                url=abs_url,
                callback=self.parse,
                meta={
                    'state_name': state_name,
                }
        )

    def parse(self, response):
        yield {
            'State_Name': response.request.meta['state_name'],
            'State_Capital': response.xpath("normalize-space(//a[text()='State Capital']/parent::div/parent::div/following-sibling::div/span/a/text())").get(),
            'State_Motto': response.xpath("normalize-space(//a[text()='State Motto']/parent::div/parent::div/following-sibling::div/span/a/text())").get(),
            'State_Flower': response.xpath("normalize-space(//a[text()='State Flower']/parent::div/parent::div/following-sibling::div/span/a/text())").get(),
            'State_Bird': response.xpath("normalize-space(//a[text()='State Bird']/parent::div/parent::div/following-sibling::div/span/a/text())").get(),
            'State_Amphibian': response.xpath("normalize-space(//a[text()='State Amphibian']/parent::div/parent::div/following-sibling::div/span/a/text())").get(),
            'State_Fossil': response.xpath("normalize-space(//a[text()='State Fossil']/parent::div/parent::div/following-sibling::div/span/a/text())").get(),
            'State_Fresh_Water_Fish': response.xpath("normalize-space(//a[text()='State Freshwater Fish']/parent::div/parent::div/following-sibling::div/span/a/text())").get(),
            'State_Fish': response.xpath("normalize-space(//a[text()='State Fish']/parent::div/parent::div/following-sibling::div/span/a/text())").get(),
            'State_Game_Bird': response.xpath("normalize-space(//a[text()='State Game Bird']/parent::div/parent::div/following-sibling::div/span/a/text())").get(),
            'State_Gemstone': response.xpath("normalize-space(//a[text()='State Gemstone']/parent::div/parent::div/following-sibling::div/span/a/text())").get(),
            'State_Insect': response.xpath("normalize-space(//a[text()='State Insect']/parent::div/parent::div/following-sibling::div/span/a/text())").get(),
            'State_Mammal': response.xpath("normalize-space(//a[text()='State Mammal']/parent::div/parent::div/following-sibling::div/span/a/text())").get(),
            'State_Mineral': response.xpath("normalize-space(//a[text()='State Mineral']/parent::div/parent::div/following-sibling::div/span/a/text())").get(),
            'State_Nut': response.xpath("normalize-space(//a[text()='State Nut']/parent::div/parent::div/following-sibling::div/span/a/text())").get(),
            'State_Reptile': response.xpath("normalize-space(//a[text()='State Reptile']/parent::div/parent::div/following-sibling::div/span/a/text())").get(),
            'State_Rock': response.xpath("normalize-space(//a[text()='State Rock']/parent::div/parent::div/following-sibling::div/span/a/text())").get(),
            'State_Soil': response.xpath("normalize-space(//a[text()='State Soil']/parent::div/parent::div/following-sibling::div/span/a/text())").get(),
            'State_Tree': response.xpath("normalize-space(//a[text()='State Tree']/parent::div/parent::div/following-sibling::div/span/a/text())").get(),
            'State_Tree_Fruit': response.xpath("normalize-space(//a[text()='State Tree Fruit']/parent::div/parent::div/following-sibling::div/span/a/text())").get(),
            'State_Wild_Flower': response.xpath("normalize-space(//a[text()='State Wildflower']/parent::div/parent::div/following-sibling::div/span/a/text())").get(),
            'URL': response.url
        }
