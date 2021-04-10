import scrapy


class PmonSpider(scrapy.Spider):
    name = 'pmon'

    def start_requests(self):
        yield scrapy.Request(
            url="https://www.plazajapan.com/pokemon-center-original/",
            callback=self.web1_prod_listings
        )

    def web1_prod_listings(self, response):
        prodUrls = response.xpath("(//ul[contains(@class, 'productGrid')])[last()]/li[@class='product']//h4/a/@href").getall()
        for prodUrl in prodUrls:
            yield scrapy.Request(
                url=prodUrl,
                callback=self.web1_prod_details
            )       

        #-- Handling Pagination --#
        nextPage = response.xpath("//a[contains(text(), 'Next')]/@href").get()
        if nextPage:
            yield scrapy.Request(
                url=nextPage,
                callback=self.web1_prod_listings
            )

    def web1_prod_details(self, response):
        upc = response.url.split("/")[-2]
        stock = "Out of stock"
        if response.xpath("//input[contains(@id, 'form-action-buyNow')]").get():
            stock = "In Stock"

        if stock != "Out of stock":
            yield scrapy.Request(
                url=f"https://www.pokemoncenter-online.com/?p_cd={upc}",
                callback=self.web2_stock_status,
                meta={
                    'upc': upc,
                    'stock': stock
                }            
            )

    def web2_stock_status(self, response):
        stock1 = response.request.meta['stock']
        upc = response.request.meta['upc']
        stock2 = "Out of stock"
        if response.xpath("//td/img[contains(@src, 'btn_cart.jpg')]").get():
            stock2 = "In Stock"

        yield{
            'Upc': upc,
            'Stock': stock2,
        }