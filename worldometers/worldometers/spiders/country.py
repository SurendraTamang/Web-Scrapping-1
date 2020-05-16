# -*- coding: utf-8 -*-
import scrapy
import logging


class CountrySpider(scrapy.Spider):
    name = 'country'
    allowed_domains = ['www.worldometers.info']
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        #title = response.xpath("//h1/text()").get()
        countries = response.xpath("//td/a")
        for country in countries:
            name = country.xpath(".//text()").get()
            link = country.xpath(".//@href").get()

            # absolute_url = f"https://www.worldometers.info{link}" => 1) Conversion of Relaative url to Absolute Url
            #absolute_url = response.urljoin(link) => 2) Conversion of Relaative url to Absolute Url

            #yield scrapy.Request(url = absolute_url) => It takes an absolute URL

            # yield {
            #     "country_name": name,
            #     "country_link": link
            # }

            yield response.follow(url=link, callback=self.parse_country, meta={'country_name': name})       #It takes an relative url

    def parse_country(self, response):
        #logging.info(response.url) => Displaying the output on console
        name = response.request.meta['country_name']
        rows = response.xpath("(//table[@class='table table-striped table-bordered table-hover table-condensed table-list'])[1]/tbody/tr")
        for row in rows:
            year = row.xpath(".//td/text()").get()
            population = row.xpath(".//td/strong/text()").get()

            yield {
                "country_name": name,
                "year": year,
                "population": population
            }
