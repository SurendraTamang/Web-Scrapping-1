# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class SfarmsSpider(CrawlSpider):
    name = 'sfarms'
    start_urls = ['https://www.statefarm.com/agent/us']

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//div[@class='sfx-text ']/a")),
        Rule(LinkExtractor(restrict_xpaths="//div[@class='sfx-text ']/a")),
        Rule(LinkExtractor(restrict_xpaths="//a[@class='block remove-underline']"), callback='parse_item', follow=True),
    )

    def emailGenerator(self, value):
        try:
            li = value.split(' ')
            email = f"{li[0].lower()}.{li[1].lower()}@statefarm.com"
            return email
        except:
            return "NA"

    def addressUrl(self, value):
        try:
            if value:
                absolute_url = f"https://www.statefarm.com{value}"
                return absolute_url
            else:
                return value
        except:
            return value

    def parse_item(self, response):
     
        yield {
            'company-name': response.xpath("//span[@id='AgencyInformationLabelId']/span/text()").get(),
            'agent-name': response.xpath("//span[@id='AgentNameLabelId']/span/text() | //h2[@id='AgentNameLabelId']/span/text()").get(),
            'email': self.emailGenerator(response.xpath("//span[@id='AgentNameLabelId']/span/text() | //h2[@id='AgentNameLabelId']/span/text()").get()),
            'phone-no1': response.xpath("normalize-space(//div[@class='hidden-phone']/span/span/text() | //span[@id='offNumber_tab_mainLocContent_0']/span/text())").get(),
            'phone-no2': response.xpath("normalize-space(//span[@id='offNumber_tab_additionalLocContent_0_0']/span/text())").get(),
            'fax-no': response.xpath("//div[@itemprop='faxNumber']/span/text()").get(),
            'landmark': response.xpath("//p[@id='landmarkId']/text()").get(),
            'zip-code': response.xpath("normalize-space((//div[@class='locationText'])[1]/div[2]/span/span[3]/text())").get(),
            'state': response.xpath("normalize-space((//div[@class='locationText'])[1]/div[2]/span/span[2]/text())").get(),
            'city': response.xpath("normalize-space((//div[@class='locationText'])[1]/div[2]/span/span[1]/text())").get(),
            'street': response.xpath("normalize-space(concat((//div[@class='locationText'])[1]/div[1]/span/text(), ' ', (//div[@class='locationText'])[1]/div[1]/span/text()[preceding-sibling::br]))").get(),
            'address-url': self.addressUrl(response.xpath("((//div[@class='locationText'])[2]/b/a/@href)[1]").get()),
            #'secondary-address': response.xpath("normalize-space(concat((//div[@class='locationText'])[4]/div[1]/span/text(), ' ', (//div[@class='locationText'])[4]/div[1]/span/text()[preceding-sibling::br], ' ', (//div[@class='locationText'])[4]/div[2]/span/span[1]/text(), ' ', (//div[@class='locationText'])[4]/div[2]/span/span[2]/text(), ' ', (//div[@class='locationText'])[4]/div[2]/span/span[3]/text()))").get(),
            #'secondary-address-url': self.addressUrl(response.xpath("((//div[@class='locationText'])[5]/b/a/@href)[1]").get()),
            'agents-url': response.xpath("//a[@title='Agent Redirect URL']/@href").get()
        }