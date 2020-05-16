# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from scrapy.selector import Selector
import json
from ..items import SteamstoreItem


class GamesSpider(scrapy.Spider):
    name = 'games'
    allowed_domains = ['store.steampowered.com']
    # start_urls = ['https://store.steampowered.com/search/?filter=topsellers/']
    start_position = 0
    end_position = 50   

    def start_requests(self):
        yield scrapy.Request(
            url='https://store.steampowered.com/search/results/?query&start=0&count=50&dynamic_data=&sort_by=_ASC&snr=1_7_7_topsellers_7&filter=topsellers&infinite=1',
            #url='https://store.steampowered.com/search/results/?query&start=0&count=50&dynamic_data=&sort_by=_ASC&snr=1_7_7_230_7&infinite=1',
            method='POST',
            callback=self.parse
        )

    def parse(self, response):
        #steam_item = SteamstoreItem()
        response_dict = json.loads(response.body)
        html = response_dict.get('results_html')
        # with open('index.html', 'w', encoding='utf8') as f:
        #     f.write(html)
        sel = Selector(text=html)
        games = sel.xpath("//body/a")
        for game in games:
            loader = ItemLoader(item=SteamstoreItem(), selector=game, response=response)
            loader.add_xpath("game_url", ".//@href")
            loader.add_xpath("img_url", ".//div/img/@src")
            loader.add_xpath("game_name", ".//span[@class='title']/text()")
            loader.add_xpath("release_date", ".//div[contains(@class, 'search_released')]/text()")
            loader.add_xpath("platforms", ".//p/span[contains(@class, 'platform_img') or @class='vr_required' or @class='vr_supported']/@class")
            loader.add_xpath("rating", ".//span[contains(@class, 'search_review_summary')]/@data-tooltip-html")
            loader.add_xpath("original_price", ".//div[contains(@class, 'search_price_discount_combined')]")
            loader.add_xpath("discounted_price", "normalize-space((.//div[contains(@class, 'search_price discounted')]/text())[2])")
            loader.add_xpath("discounted_rate", ".//div[contains(@class, 'search_discount')]/span/text()")
            
            # steam_item['game_url'] = game.xpath(".//@href").get()
            # steam_item['img_url'] = game.xpath(".//div/img/@src").get()
            # steam_item['game_name'] = game.xpath(".//span[@class='title']/text()").get()
            # steam_item['release_date'] = game.xpath(".//div[contains(@class, 'search_released')]/text()").get()
            # steam_item['platforms'] = self.get_platforms(game.xpath(".//p/span[contains(@class, 'platform_img') or @class='vr_required' or @class='vr_supported']/@class").getall())
            # steam_item['rating'] = self.clean_html_text(game.xpath(".//span[contains(@class, 'search_review_summary')]/@data-tooltip-html").get())
            # steam_item['original_price'] = self.get_original_price(game.xpath(".//div[contains(@class, 'search_price_discount_combined')]"))
            # steam_item['discounted_price'] = game.xpath("normalize-space((.//div[contains(@class, 'search_price discounted')]/text())[2])").get()
            # steam_item['discounted_rate'] = self.clean_discount_rate(game.xpath(".//div[contains(@class, 'search_discount')]/span/text()").get())
            # #Next button element => //a[@class='pagebtn' and text()='text']
            # yield steam_item

            yield loader.load_item()

        total_count = response_dict.get('total_count')     

        if self.end_position < total_count:
            self.start_position += 50
            self.end_position += 50
            yield scrapy.Request(
                url=f'https://store.steampowered.com/search/results/?query&start={self.start_position}&count=50&dynamic_data=&sort_by=_ASC&snr=1_7_7_topsellers_7&filter=topsellers&infinite=1',
                method='POST',
                callback=self.parse
            )