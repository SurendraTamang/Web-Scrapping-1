# -*- coding: utf-8 -*-
import scrapy


class Mitchell24850Spider(scrapy.Spider):
    name = 'Mitchell_24850'

    def filter_text(self, value):
        li = []
        try:
            li = value.split("-")
            return li
        except:
            return None
    
    def start_requests(self):
        yield scrapy.Request(
            url="https://www.mitchellshire.vic.gov.au/planning-and-building/planning-services/advertised-planning-applications",
            callback=self.listings
        )

    def listings(self, response):
        listings = response.xpath("//ul[@class='child-list']/li")
        for lists in listings:
            li = self.filter_text(lists.xpath("normalize-space(.//h3/text())").get())
            url = lists.xpath(".//a/@href").get()
            activity = lists.xpath("normalize-space(.//div[@class='child__description']/text())").get()
            if len(li) > 1:
                yield{
                    'appNum': li[0],
                    'nameLGA': 'Mitchell',
                    'codeLGA': '24850',
                    'address': li[1],
                    'activity': activity,
                    'applicant': None,
                    'lodgeDate': None,
                    'decisionDate': None,
                    'status': None,
                    'url': url
                }
            else:
                yield scrapy.Request(
                    url=url,
                    callback=self.parse,
                    meta={
                        'activity': activity,
                        'address': lists.xpath("normalize-space(.//h3/text())").get()
                    }
                )

    def parse(self, response):
        yield{
            'appNum': response.xpath("//li[text()='state the VCAT reference number ']/strong/text()").get(),
            'nameLGA': 'Mitchell',
            'codeLGA': '24850',
            'address': response.request.meta['address'],
            'activity': response.request.meta['activity'],
            'applicant': None,
            'lodgeDate': None,
            'decisionDate': None,
            'status': None,
            'url': response.url
        }
        