# -*- coding: utf-8 -*-
import scrapy


class AdvocateSpider(scrapy.Spider):
    name = 'advocate'
    # allowed_domains = ['members.calbar.ca.gov']
    # start_urls = ['http://members.calbar.ca.gov/']

    def start_requests(self):
        yield scrapy.Request(
            url='http://members.calbar.ca.gov/fal/LicenseeSearch/QuickSearch?FreeText=all&SoundsLike=false#',
            callback=self.follow_links
        )
    
    def follow_links(self, response):
        items = response.xpath("//tbody/tr[@class='rowASRLodd']")
        for item in items:
            status = item.xpath("normalize-space(.//td[2]/text())").get()
            if status == 'Active':
                name = item.xpath("normalize-space(.//td/a/text())").get()
                rel_url = item.xpath(".//td/a/@href").get()
                abs_url = f"http://members.calbar.ca.gov{rel_url}"
                yield scrapy.Request(
                    url=abs_url,
                    callback=self.parse,
                    meta={
                        'Name': name,
                        'Status': status
                    }
                )
            else:
                pass

    def parse(self, response):
        name = response.request.meta['Name']
        status = response.request.meta['Status']
        yield {
            'Name': name,
            'Status': status,
            'Url': response.url
        }
