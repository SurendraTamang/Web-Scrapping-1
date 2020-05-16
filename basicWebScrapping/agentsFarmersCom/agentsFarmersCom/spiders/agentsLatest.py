# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class AgentslatestSpider(scrapy.Spider):
    name = 'agentsLatest'
    start_urls = ['https://agents.farmers.com/nj?Source_Indicator=AP']

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//ul[@class='Directory-listLinks']/li/a"), callback='parse_item', follow=True)
        #Rule(LinkExtractor(restrict_xpaths="//ul[@class='Directory-listLinks']/li/a"), callback='parse_item', follow=True)
        #Rule(LinkExtractor(restrict_xpaths="//span[@class='location-title-nameWrapper']/a"), callback='parse_item', follow=True)
    )

    def emailGenerator1(self, value):
        try:
            li = value.split(' ')
            email = f"{li[0].lower()}.{li[1].lower()}@farmers.com"
            return email
        except:
            return "NA"

    def emailGenerator2(self, value):
        try:
            li = value.split(' ')
            email = f"{li[0].lower()}{li[1].lower()}@farmers.com"
            return email
        except:
            return "NA"

    def emailGenerator3(self, value):
        try:
            li = value.split(' ')
            email = f"{li[0].lower()[:1]}{li[1].lower()}@farmers.com"
            return email
        except:
            return "NA"

    def emailGenerator4(self, value):
        try:
            li = value.split(' ')
            email = f"{li[1].lower()}@farmers.com"
            return email
        except:
            return "NA"

    def userReviews(self, value):
        try:
            li = value.split(' ')
            if li[0]:
                return int(li[0])
            else:
                return 0
        except:
            return 0

    def ratingsFloatConvert(self, value):
        try:
            if value:
                return float(value)
            else:
                return 0
        except:
            return 0

    def parse_item(self, response):
        yield {
            'agent_name': response.xpath("//h1[@class='location-name Heading--impactInvert']/text()").get(),
            'phone_no': response.xpath("(//a[@data-ya-track='phone']/text())[2]").get(),
            'fax_no': response.xpath("//span[@class='c-phone-number-span c-phone-fax-number-span c-phone-number-span-nolink']/text()").get(),
            'ratings': self.ratingsFloatConvert(response.xpath("(//span[@class='c-ReviewsSummary-number']/text())[1]").get()),
            'noOfUserReviews': self.userReviews(response.xpath("(//a[@class='Link About-reviewsLink']/text())[1]").get()),
            'zip': response.xpath("//div[@class='c-AddressRow']/span[@class='c-address-postal-code']/text()").get(),
            'state_code': response.xpath("//div[@class='c-AddressRow']/abbr[@class='c-address-state']/text()").get(),
            'state_name': response.xpath("(//div[@class='c-AddressRow']/abbr/@title)[1]").get(),
            'city': response.xpath("//div[@class='c-AddressRow']/span[@class='c-address-city']/text()").get(),
            'street': response.xpath("concat(//span[@class='c-address-street-1']/text(), ' ', //span[@class='c-address-street-2']/text())").get(),
            'email_38_accuracy': self.emailGenerator1(response.xpath("//h1[@class='location-name Heading--impactInvert']/text()").get()),
            'email_14_accuracy': self.emailGenerator2(response.xpath("//h1[@class='location-name Heading--impactInvert']/text()").get()),
            'email_12_accuracy': self.emailGenerator3(response.xpath("//h1[@class='location-name Heading--impactInvert']/text()").get()),
            'email_11_accuracy': self.emailGenerator4(response.xpath("//h1[@class='location-name Heading--impactInvert']/text()").get())
        }

