# -*- coding: utf-8 -*-
import scrapy
import json


class IndgSpider(scrapy.Spider):
    name = 'indg'
    cntr = 1

    def genPayload(self, page):
        rPayload = {
            "category_main": "Video Games",
            "category_top_level": "Creative Works",
            "project_timing": "all",
            "project_type": "campaign",
            "page_num": page,
            "per_page": 999,
            "sort": "most_funded",
            "q": "",
            "tags": []
        }
        return rPayload

    def start_requests(self):
        yield scrapy.Request(
            url='https://www.indiegogo.com/private_api/discover',
            headers={
                'Content-Type': 'application/json'
            },
            body=json.dumps(self.genPayload(1)),
            method='POST',
            callback=self.parse
        )

    def parse(self, response):           
        json_resp = json.loads(response.body)
        items = json_resp.get('response').get('discoverables')
        for item in items:
            yield{
                'Titile': item.get("title"),
                'Url': f"https://www.indiegogo.com{item.get('clickthrough_url')}"
            }
        
        self.cntr += 1
        yield scrapy.Request(
            url='https://www.indiegogo.com/private_api/discover',
            headers={
                'Content-Type': 'application/json'
            },
            body=json.dumps(self.genPayload(self.cntr)),
            method='POST',
            callback=self.parse
        )
