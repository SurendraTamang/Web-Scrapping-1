import scrapy
import json


class RatemyagentscraperSpider(scrapy.Spider):
    name = 'ratemyagentScraper'

    def start_requests(self):
        yield scrapy.Request(
            url='https://api.ratemyagent.com.au/Sales/Locations/States/2/Agents?StatisticType=TotalRecommendations&skip=0&take=20',
            method='GET',
            callback=self.parse
        )

    def parse(self, response):
        json_resp = json.loads(response.body)
        items = json_resp.get('Results')
        for item in items:
            print(item.get('Name'))
            print(item.get('Mobile'))
