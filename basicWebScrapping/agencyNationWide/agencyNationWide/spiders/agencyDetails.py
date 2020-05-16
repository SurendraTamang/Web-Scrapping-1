# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class AgencydetailsSpider(CrawlSpider):
    name = 'agencyDetails'
    #allowed_domains = ['https://agency.nationwide.com']
    start_urls = ['https://agency.nationwide.com']

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//li[@class='Directory-listItem']/a")),
        Rule(LinkExtractor(restrict_xpaths="//li[@class='Directory-listItem']/a")),
        Rule(LinkExtractor(restrict_xpaths="//a[@class='Teaser-titleLink']"), callback='parse_item', follow=True)
    )

    def removeCharacters(self, value):
        try:
            if '=' in value:
                return value.split('=')[1]
            else:
                return value
        except:
            return value

    def parse_item(self, response):
        yield {
            'company-name': response.xpath("//h1[@class='Core-title']/span/text() | //h1[@class='CoreExclusive-title']/span/text()").get(),
            'agent-name': response.xpath("//p[@class='CoreExclusive-agentName']/text()").get(),
            'email': self.removeCharacters(response.xpath("(//@data-email)[1] | //div[@class='c-Modal-messageWrapper']/iframe/@src").get()),
            'ph_no-main': response.xpath("//a[@class='c-phone-number-link c-phone-main-number-link']/text()").get(),
            'fax-no': response.xpath("//span[@class='c-phone-number-span c-phone-fax-number-span']/text()").get(),
            'website-address': response.xpath("//a[@class='Core-websiteLink']/@href").get(),
            'googleMapsLinks': response.xpath("//address[@class='c-address']/a/@href").get(),
            'street_name': response.xpath("concat((//span[@class='c-address-street-1'])[1], ' ', (//span[@class='c-address-street-2'])[1])").get(),
            'city': response.xpath("(//span[@class='c-address-city']/text())[1]").get(),
            'state': response.xpath("(//div[@class='c-AddressRow']/abbr/@title)[1]").get(),
            'zip': response.xpath("(//span[@itemprop='postalCode']/text())[1]").get()
            #'physicalAddress': response.xpath("concat((//div[@class='c-AddressRow']/span/text())[1], ' ', (//div[@class='c-AddressRow']/span/text())[2], ' ', (//div[@class='c-AddressRow']/span/text())[3], ' ', (//div[@class='c-AddressRow']/span/text())[4], ' ', (//div[@class='c-AddressRow']/span/text())[5], ' ', (//div[@class='c-AddressRow']/span/text())[6])").get(),
            #'physicalAddress': response.xpath("concat(//meta[@itemprop='addressLocality']/@content, ' ', //meta[@itemprop='streetAddress']/@content)").get()
        }
