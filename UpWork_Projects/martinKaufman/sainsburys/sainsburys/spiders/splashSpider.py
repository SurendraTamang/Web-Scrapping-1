import scrapy
from scrapy_splash import SplashRequest
import pandas as pd
import re


class SplashspiderSpider(scrapy.Spider):
    name = 'splashSpider'
    
    http_user = 'admin'
    http_pass = 'admin'

    df = pd.read_excel("D:/linodeWorkspace/MartinFinished/sainsburys/check_link.xlsx")
    prodURLs = df['links'].values.tolist()

    def getQuantity(self, value):
        try:
            li = value.slpit(" ")
            result = li[-1:]
            if bool(re.search(r'\d', result)):
                return result
            else:
                result="".join(i for i in li[-2:])
                if bool(re.search(r'\d', result)):
                    return result
                else:
                    return None
        except:
            return None

    script = '''
        function main(splash, args)
            assert(splash:go(args.url))
            assert(splash:wait(2))
            splash:evaljs("window.scrollTo(0, document.body.scrollHeight);")
            return splash:html()
        end
    '''

    def start_requests(self):
        yield SplashRequest(
            url='https://www.sainsburys.co.uk/shop/gb/groceries/food-cupboard/seeall?fromMegaNav=1',
            endpoint='execute',
            callback=self.listingsPage,
            args={
                'lua_source': self.script
            }
        )

    def listingsPage(self, response):
        products = response.xpath("//li[@class='gridItem']")
        for product in products:
            prodURL = product.xpath(".//h3/a/@href").get()
            cProdURl = prodURL.replace("shop/gb/groceries/product/details", "gol-ui/product")
            if cProdURl not in self.prodURLs:
                yield SplashRequest(
                    url=prodURL,
                    endpoint='execute',
                    callback=self.parse,
                    args={
                        'lua_source': self.script
                    }
                )

        nextPage = response.xpath("//li[@class='next']/a/@href").get()
        if nextPage:
            yield SplashRequest(
                url=nextPage,
                endpoint='execute',
                callback=self.listingsPage,
                args={
                    'lua_source': self.script
                }
            )

    
    def parse(self, response):
        name = response.xpath("normalize-space(//h1/text())").get()
        sSize = response.xpath("normalize-space(//tr[@class='tableTitleRow']/th[2]/text())").get()
        if sSize  == "":
            sSize = response.xpath("normalize-space(//tr/th[2]/text())").get()
        calories = response.xpath("normalize-space(//tbody/tr[2]/td/text())").get()
        if "kcal" not in calories:
            calories = response.xpath("normalize-space(//tbody/tr/td/text())").get()
        yield {
            'Name of Food Item': name,
            'Serving Size of Food Item': sSize,
            'Price': response.xpath("normalize-space(//div[@data-test-id='pd-retail-price']/text())").get(),
            'Number of Calories Per Serving': calories,
            'Image (link)': response.xpath("//img[contains(@class, 'pd__image')]/@src").get(),
            'Product (link)': response.url,
            'Lvl1 Category': response.xpath("normalize-space(//ol/li[1]/a/text())").get(),
            'Lvl2 Category': response.xpath("normalize-space(//ol/li[2]/a/text())").get(),
            'quantity': self.getQuantity(name)
        }
