# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy_splash import SplashRequest
import json


class PropertySpider(scrapy.Spider):
    #handle_httpstatus_list = [555]
    name = 'property'
    allowed_domains = ['www.centris.ca']

    http_user = 'user'
    http_pass = 'userpass'
    #start_urls = ['http://www.centris.ca/']

    position = {
        'startPosition': 0
    }
    
    #Optimized lua script for splash
    script = '''
        function main(splash, args)
            splash:on_request(function(request)
                if request.url:find('css') then
                    request.abort()
                end
            end)
            splash.images_enabled = false
            splash.js_enabled = false
            assert(splash:go(args.url))
            assert(splash:wait(0.5))
            return splash:html()
            --return {
                --html = splash:html(),
                --png = splash:png(),
                --har = splash:har()
            --}
        end
    '''
    # script = '''
    #     function main(splash, args)
    #         assert(splash:go(args.url))
    #         assert(splash:wait(0.5))
    #         return splash:html()
    #     end
    # '''

    def start_requests(self):
        query = {
            "queryView": {
                "UseGeographyShapes": 0,
                "Filters": [
                    {
                        "MatchType": "GeographicSubArea",
                        "Text": "Montréal (North Shore)",
                        "Id": "GSGS4623"
                    }
                ],
                "FieldsValues": [
                    {
                        "fieldId": "GeographicSubArea",
                        "value": "GSGS4623",
                        "fieldConditionId": "",
                        "valueConditionId": ""
                    },
                    {
                        "fieldId": "SellingType",
                        "value": "Rent",
                        "fieldConditionId": "",
                        "valueConditionId": ""
                    },
                    {
                        "fieldId": "Category",
                        "value": "Residential",
                        "fieldConditionId": "",
                        "valueConditionId": ""
                    },
                    {
                        "fieldId": "LandArea",
                        "value": "SquareFeet",
                        "fieldConditionId": "IsLandArea",
                        "valueConditionId": ""
                    },
                    {
                        "fieldId": "RentPrice",
                        "value": 0,
                        "fieldConditionId": "ForRent",
                        "valueConditionId": ""
                    },
                    {
                        "fieldId": "RentPrice",
                        "value": 999999999999,
                        "fieldConditionId": "ForRent",
                        "valueConditionId": ""
                    }
                ]
            },
            "isHomePage": True
        }
        yield scrapy.Request(
            url='https://www.centris.ca/mvc/property/UpdateQuery',
            method='POST',
            body=json.dumps(query),
            headers={
                'Content-Type': 'application/json'
            },
            callback=self.update_query
        )

    def update_query(self, response):
        yield scrapy.Request(
            url='https://www.centris.ca/Mvc/Property/GetInscriptions',
            method='POST',
            body=json.dumps(self.position),
            headers={
                'Content-Type': 'application/json'
            },
            callback=self.parse
        )

    def parse(self, response):
        resp_dict = json.loads(response.body)
        html = resp_dict.get('d').get('Result').get('html')
        # with open('index.html', 'w') as f:
        #     f.write(html)
        sel = Selector(text=html)
        listings = sel.xpath("//div[@data-id='templateThumbnailItem']")

        for listings in listings:
            # address1 = listings.xpath("normalize-space(.//parent::span[@class='address']/child::div[1]/text())").getall()
            city = listings.xpath("normalize-space(.//parent::span[@class='address']/child::div[2]/text())").getall()
            # address3 = listings.xpath("normalize-space(.//parent::span[@class='address']/child::div[3]/text())").getall()
            rel_url = listings.xpath("normalize-space(.//a[@data-summaryurl='SummaryUrl']/@href)").get()
            price = listings.xpath("normalize-space(.//span[@itemprop='price']/text())").get()
            bed = listings.xpath("normalize-space(.//div[@class='cac']/text())").get()
            bath = listings.xpath("normalize-space(.//div[@class='sdb']/text())").get()
            category = listings.xpath("normalize-space(.//parent::span[@class='category']/child::div/text())").get()
            abs_url = f"https://www.centris.ca{rel_url}"
            yield SplashRequest(
                url=abs_url,
                endpoint='execute',
                callback=self.parse_summary,
                args={
                    'lua_source': self.script
                },
                meta={
                    'category': category,
                    'city': city,
                    'price': price,
                    'bed': bed,
                    'bath': bath,
                    'url': abs_url                    
                }
            )
            
        count = resp_dict.get('d').get('Result').get('count')
        increment_no = resp_dict.get('d').get(
            'Result').get('inscNumberPerPage')

        if self.position['startPosition'] <= count:
            self.position['startPosition'] += increment_no
            yield scrapy.Request(
                url='https://www.centris.ca/Mvc/Property/GetInscriptions',
                method='POST',
                body=json.dumps(self.position),
                headers={
                    'Content-Type': 'application/json'
                },
                callback=self.parse
            )
    def parse_summary(self, response):
        address = response.xpath("normalize-space(//h2[@itemprop='address']/text())").get()
        rooms = response.xpath("normalize-space(//div[@class='col-lg-3 col-sm-6 piece']/text())").get()
        description = response.xpath("normalize-space(//div[@itemprop='description']/text())").get()
        category = response.request.meta['category']
        city = response.request.meta['city']
        price = response.request.meta['price']
        bed = response.request.meta['bed']
        bath = response.request.meta['bath']
        url = response.request.meta['url']

        yield {
                'address': address,
                'category': category,
                'description': description,
                'features': f"{bed} bed, {bath} bath, {rooms} rooms",
                'price': price,
                'city': city,
                'url': url
            }
