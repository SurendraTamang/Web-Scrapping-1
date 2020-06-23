# -*- coding: utf-8 -*-
import scrapy
import pandas as pd


class BbprodsSpider(scrapy.Spider):
    name = 'bbProds'

    #li = [
        #'https://www.bestbuy.com/site/home/outdoor-living/pcmcat179100050006.c?id=pcmcat179100050006'
        #'https://www.bestbuy.com/site/home/batteries-power/pcmcat145100050000.c?id=pcmcat145100050000'
        #'https://www.bestbuy.com/site/mobile-cell-phones/mobile-phone-accessories/abcat0811002.c?id=abcat0811002'
        #'https://www.bestbuy.com/site/electronics/health-fitness-sports/pcmcat242800050021.c?id=pcmcat242800050021'
        #'https://www.bestbuy.com/site/electronics/home-security-safety/pcmcat254000050002.c?id=pcmcat254000050002'
        # 'https://www.bestbuy.com/site/electronics/movies-music/abcat0600000.c?id=abcat0600000',
        # 'https://www.bestbuy.com/site/electronics/car-audio-gps/abcat0300000.c?id=abcat0300000',
        # 'https://www.bestbuy.com/site/electronics/drones-toys-collectibles/pcmcat252700050006.c?id=pcmcat252700050006'
    #]

    # def start_requests(self):
    #     for item in self.li:
    #         yield scrapy.Request(
    #             url=item,
    #             callback=self.parse
    #         )

    # def parse(self, response):
        # lvl1_cat = response.xpath("(//h2)[4]/text()").get()
        # lvl2_listings = response.xpath("(//h2)[4]/following-sibling::nav/div")
        # for lvl2 in lvl2_listings:
        #     lvl2_cat = lvl2.xpath(".//h3/text()").get()
        #     lvl3_listings = lvl2.xpath(".//div")
        #     for lvl3 in lvl3_listings:
        #         lvl3_cat = lvl3.xpath(".//a/text()").get()
        #         url = f'''https://www.bestbuy.com{lvl3.xpath(".//a/@href").get()}'''
        #         yield{
        #             'lvl1_cat': lvl1_cat,
        #             'lvl2_cat': lvl2_cat,
        #             'lvl3_cat': lvl3_cat,
        #             'url': url
        #         }





        # listings = response.xpath("//div[@class='navigation-link']")
        # for lists in listings:
        #     yield{
        #         'lvl1_cat': 'Home, Furniture & Office',
        #         'lvl2_cat': 'Outdoor Living',
        #         'lvl3_cat': lists.xpath(".//a/text()").get(),
        #         'url': f'''https://www.bestbuy.com{lists.xpath(".//a/@href").get()}'''
        #     }



        # lvl1_cat = response.xpath("//h1[@class='page-title']/text()").get()
        # print(lvl1_cat)
        # lvl1_listings = response.xpath("//div[contains(@class, 'vn-panel col-xs-4')]")
        # print(lvl1_listings)
        # for lvl2 in lvl1_listings:
        #     lvl2_cat = lvl2.xpath("normalize-space(.//h3/a/text())").get()
        #     lvl2_listings = lvl2.xpath(".//div[@class='row']//li")
        #     for lvl3 in lvl2_listings:
        #         yield{
        #             'lvl1_cat' : lvl1_cat,
        #             'lvl2_cat' : lvl2_cat,
        #             'lvl3_cat' : lvl3.xpath("normalize-space(.//a/text())").get(),
        #             'url' : f'''https://www.bestbuy.com{lvl3.xpath(".//a/@href").get()}'''
        #         }
    




                 #   CODE FOR DATA EXTRACTION    #

    df = pd.read_excel("/root/byom/linodeWorkspace/bestby/links.xlsx")
    #df = pd.read_excel("D:/sipun/Web-Scrapping/UpWork_Projects/andy_upwork/bestby/links.xlsx")

    def start_requests(self):
        for _, value in self.df.iterrows():
            yield scrapy.Request(
                url=value['url'],
                callback=self.parse,
                meta={
                    'lvl1_cat': value['lvl1_cat'],
                    'lvl2_cat': value['lvl2_cat'],
                    'lvl3_cat': value['lvl3_cat']
                }
            )

    def parse(self, response):
        lvl1_cat = response.request.meta['lvl1_cat']
        lvl2_cat = response.request.meta['lvl2_cat']
        lvl3_cat = response.request.meta['lvl3_cat']
        prod_listings = response.xpath("//ol[@class='sku-item-list']/li")
        for prod in prod_listings:
            yield {
                'product_name': prod.xpath("normalize-space(.//h4/a/text())").get(),
                'price': prod.xpath("normalize-space(.//div[contains(@class, 'priceView-customer-price')]/span[1]/text())").get(),
                'lvl1_cat': lvl1_cat,
                'lvl2_cat': lvl2_cat,
                'lvl3_cat': lvl3_cat,                
                'url': f'''https://www.bestbuy.com{prod.xpath(".//h4/a/@href").get()}'''
            }

        next_page = response.xpath("//a[@class='sku-list-page-next']/@href").get()
        if next_page:
            yield scrapy.Request(
                url=next_page,
                callback=self.parse,
                meta={
                    'lvl1_cat': lvl1_cat,
                    'lvl2_cat': lvl2_cat,
                    'lvl3_cat': lvl3_cat
                }
            )
