# -*- coding: utf-8 -*-
import pandas as pd
import scrapy
from scrapy.loader import ItemLoader
from scrapy_splash import SplashRequest
from ..items import GimagesItem


class ImagesSpider(scrapy.Spider):
    name = 'images'

    http_user = 'user'
    http_pass = 'userpass'

    df = pd.read_excel('D:/upworkWorkspace/Testing/set1.xlsx', sheet_name='sheet1')
    #df = pd.read_excel('D:/upworkWorkspace/Testing/gImages/input.xlsx')
    #place_list = df['place_name'].tolist()

    script = '''
        function main(splash, args)
            splash:on_request(function(request)
                if request.url:find('css') then
                    request.abort()
                end
            end)
            splash.images_enabled = false
            assert(splash:go(args.url))
            assert(splash:wait(0.5))
            return splash:html()
        end
    '''

    def generate_url(self, place):
        str_new = place.replace(',','').replace('"', '').replace("'", '').replace(':', '').rstrip().split(' ')
        return f'''https://www.google.com/search?q={'+'.join(str_new)}&tbm=isch&ved=2ahUKEwjt7dSSsOPoAhXKGnIKHWcWBBEQ2-cCegQIABAA&oq={'+'.join(str_new)}&gs_lcp=CgNpbWcQDFAAWABgiq2sAWgAcAB4AIABAIgBAJIBAJgBAKoBC2d3cy13aXotaW1n&sclient=img&ei=8kqTXu2sCMq1yAPnrJCIAQ&bih=667&biw=1349&rlz=1C1RLNS_enIN893IN893&tbs=sur%3Afmc&hl=en'''

    def start_requests(self):
        for _, value in self.df.iterrows():
            lat = str(value['lat'])
            long = str(value['long'])
            name = value['name']
            query = value['query']
            yield SplashRequest(
                url=self.generate_url(query),
                endpoint='execute',
                callback=self.follow_url,
                args={
                    'lua_source': self.script
                },
                meta={
                    'place_name': name,
                    'latitude': lat,
                    'longitude': long
                }
            )

    def follow_url(self, response):
        place_name = response.request.meta['place_name']
        lat = response.request.meta['latitude']
        long = response.request.meta['longitude']
        cntr = 0
        for i in range(1,17):
            listings = response.xpath(f"(//div[contains(@class, 'isv-r')])[{i}]")

            flickr_url = listings.xpath(".//div[text()='flickr.com']/parent::div/parent::a/@href").get()
            wikimedia_url = listings.xpath(".//div[text()='commons.wikimedia.org']/parent::div/parent::a/@href").get()            
            nps_gov_url = listings.xpath(".//div[text()='nps.gov']/parent::div/parent::a/@href").get()       
            geo_uk_url = listings.xpath(".//div[text()='geograph.org.uk']/parent::div/parent::a/@href").get()       
        
            try:
                if geo_uk_url:
                    cntr += 1
                    if cntr <= 5:        
                        yield scrapy.Request(
                            url=geo_uk_url,
                            callback=self.parse,
                            meta={
                                'file_name': f"{place_name}_{lat}{long}_{i}_Park Search Shop",
                                'place_name': place_name,
                                'latitude': lat,
                                'longitude': long
                            }
                        )   
                    else:
                        break
                elif wikimedia_url:
                    cntr += 1
                    if cntr <= 5:        
                        yield scrapy.Request(
                            url=wikimedia_url,
                            callback=self.parse,
                            meta={
                                'file_name': f"{place_name}_{lat}{long}_{i}_Park Search Shop",
                                'place_name': place_name,
                                'latitude': lat,
                                'longitude': long
                            }
                        )   
                    else:
                        break
                elif flickr_url:
                    cntr += 1
                    if cntr <= 5:                    
                        yield scrapy.Request(
                            url=flickr_url,
                            callback=self.parse,
                            meta={
                                'file_name': f"{place_name}_{lat}{long}_{i}_Park Search Shop",
                                'place_name': place_name,
                                'latitude': lat,
                                'longitude': long
                            }   
                        )
                    else:
                        break
                elif nps_gov_url:
                    cntr += 1
                    if cntr <= 5:
                        yield scrapy.Request(
                            url=nps_gov_url,
                            callback=self.parse,
                            meta={
                                'file_name': f"{place_name}_{lat}{long}_{i}_Park Search Shop",
                                'place_name': place_name,
                                'latitude': lat,
                                'longitude': long
                            }   
                        )
                    else:
                        break
            except:
                pass

    def parse(self, response):
        loader = ItemLoader(item=GimagesItem())

        wmedia_url = response.xpath("//div[@class='fullImageLink']//img/@src").get()
        flickr_url = response.xpath("//img[@class='main-photo']/@src").get()
        nps_gov_url = response.xpath("(//figure/img/@src)[1]").get()
        geo_uk_url = response.xpath("//div[@class='shadow shadow_large']//img/@src").get()

        if wmedia_url:
            loader.add_value('place_name', response.request.meta['place_name'])
            loader.add_value('latitude', response.request.meta['latitude'])
            loader.add_value('longitude', response.request.meta['longitude'])
            loader.add_value('file_name', f"{response.request.meta['file_name']}.jpg")
            loader.add_value('image_urls', wmedia_url)
        elif flickr_url:
            loader.add_value('place_name', response.request.meta['place_name'])
            loader.add_value('latitude', response.request.meta['latitude'])
            loader.add_value('longitude', response.request.meta['longitude'])
            loader.add_value('file_name', f"{response.request.meta['file_name']}.jpg")
            loader.add_value('image_urls', f"https:{flickr_url}")
        elif nps_gov_url:
            loader.add_value('place_name', response.request.meta['place_name'])
            loader.add_value('latitude', response.request.meta['latitude'])
            loader.add_value('longitude', response.request.meta['longitude'])
            loader.add_value('file_name', f"{response.request.meta['file_name']}.jpg")
            loader.add_value('image_urls', f"https://www.nps.gov{nps_gov_url}")
        elif geo_uk_url:
            loader.add_value('place_name', response.request.meta['place_name'])
            loader.add_value('latitude', response.request.meta['latitude'])
            loader.add_value('longitude', response.request.meta['longitude'])
            loader.add_value('file_name', f"{response.request.meta['file_name']}.jpg")
            loader.add_value('image_urls', geo_uk_url)
        else:
            loader.add_value('place_name', response.request.meta['place_name'])
            loader.add_value('latitude', response.request.meta['latitude'])
            loader.add_value('longitude', response.request.meta['longitude'])
            loader.add_value('file_name', f"{response.request.meta['file_name']}.jpg")
            loader.add_value('image_urls', None)

        yield loader.load_item()
