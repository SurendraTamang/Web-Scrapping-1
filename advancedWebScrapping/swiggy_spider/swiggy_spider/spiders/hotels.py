# -*- coding: utf-8 -*-
import scrapy
import json


class HotelsSpider(scrapy.Spider):
    name = 'hotels'
    allowed_domains = ['www.swiggy.com']
    # start_urls = ['http://www.swiggy.com/']

    def price_to_rupees(self, value):
        price = str(value)
        try:
            return f"Rs.{price[:-2]}"
        except:
            return "NA"

    def start_requests(self):
        counter = 0
        for _ in range(13):
            link = f'https://www.swiggy.com/dapi/restaurants/list/v5?lat=19.1364016&lng=72.8296252&offset={counter}&sortBy=RELEVANCE&pageType=SEE_ALL&page_type=DESKTOP_SEE_ALL_LISTING'
            counter += 15
            yield scrapy.Request(
                url=link,
                callback=self.menu_details
            )

    def menu_details(self, response):
        try:
            resp_dict = json.loads(response.body)
            hotels = resp_dict.get('data').get('cards')
            for hotel in hotels:
                id = hotel.get('data').get('data').get('id')
                name = hotel.get('data').get('data').get('name')
                area = hotel.get('data').get('data').get('area')
                link = f"https://www.swiggy.com/dapi/menu/quick?menuId={id}&categories=true"
                yield scrapy.Request(
                    url=link,
                    callback=self.parse,
                    meta={
                        'name': name,
                        'area': area
                    }
                )
        except:
            pass

    def parse(self, response):
        name = response.request.meta['name']
        area = response.request.meta['area']
        resp_dict = json.loads(response.body)
        menu = resp_dict.get('data').get('menu').get('items')
        for key in menu:
            dish = resp_dict.get('data').get('menu').get('items').get(key).get('name')
            price = resp_dict.get('data').get('menu').get('items').get(key).get('price')
            if resp_dict.get('data').get('menu').get('items').get(key).get('isVeg'):
                category = "Veg"
            else:
                category = "Non-Veg"
            
            yield{                
                'Dish_name': dish,
                'Price': self.price_to_rupees(price),
                'Category': category,
                'Hotel_name': name,
                'Area': area
            }
            
