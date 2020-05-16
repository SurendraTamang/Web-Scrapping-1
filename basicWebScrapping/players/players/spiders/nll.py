# -*- coding: utf-8 -*-
import scrapy


class NllSpider(scrapy.Spider):
    name = 'nll'
    start_urls = ['https://www.nll.com/players/']

    def parse(self, response):
        #google_link = 'https://www.google.com/'
        players = response.xpath("//tr[@class='page-roster__player-links']")
        for player in players:
            name = player.xpath("normalize-space(.//td/a/text())").get()
            team = player.xpath("normalize-space(.//td[3]/text())").get()
            jersey = player.xpath("normalize-space(.//td[4]/text())").get()
        
            yield {
                'search_param': name+" "+jersey+" "+team+" instagram",
                'player_name': name
            }