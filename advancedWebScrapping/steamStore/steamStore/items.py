# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.selector import Selector
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from w3lib.html import remove_tags

def clean_html_text(value):
    cleaned_text = ''
    try:
        cleaned_text = remove_tags(value)
    except:
        cleaned_text = "No Reviews"
    return cleaned_text

def get_platforms(value):
    platforms = []    
    platform = value.split(" ")[-1]
    if platform == 'win':
        platforms.append('Windows')
    if platform == 'mac':
        platforms.append('Mac OS')
    if platform == 'linux':
        platforms.append('Linux')
    if platform == 'vr_required':
        platforms.append('VR Only')
    if platform == 'vr_supported':
        platforms.append('VR Supported')
    return platforms

def get_original_price(html_string):
    original_price = ''
    selector_obj = Selector(text=html_string)
    opWithDisc = selector_obj.xpath(".//div[contains(@class, 'discounted')]/span/strike/text()").get()
    if opWithDisc != None:
        original_price = opWithDisc
    else:
        original_price =  selector_obj.xpath("normalize-space(.//div[@class='col search_price  responsive_secondrow']/text())").get()
        # Sometimes normalize-space don't work, so we can use str.strip inside input_processor
    return original_price

def clean_discount_rate(value):
        if value != None:
            result = value.lstrip('-')
        else:
            result = "0%"
        return result


class SteamstoreItem(scrapy.Item):
    game_url = scrapy.Field(
        output_processor = TakeFirst()
    )
    img_url = scrapy.Field(
        output_processor = TakeFirst()
    )
    game_name = scrapy.Field(
        output_processor = TakeFirst()
    )
    release_date = scrapy.Field(
        output_processor = TakeFirst()
    )
    platforms = scrapy.Field(
        input_processor = MapCompose(get_platforms)
    )
    rating = scrapy.Field(
        input_processor = MapCompose(clean_html_text),
        output_processor = TakeFirst()
    )
    original_price = scrapy.Field(
        input_processor = MapCompose(get_original_price, str.strip),
        output_processor = Join('')
    )
    discounted_price = scrapy.Field(
        output_processor = TakeFirst()
    )
    discounted_rate = scrapy.Field(
        input_processor = MapCompose(clean_discount_rate),
        output_processor = TakeFirst()
    )
