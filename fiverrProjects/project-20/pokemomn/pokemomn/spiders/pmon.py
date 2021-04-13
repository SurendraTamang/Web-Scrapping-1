import scrapy


class PmonSpider(scrapy.Spider):
    
    name = 'pmon'

    def start_requests(self):
        yield scrapy.Request(
            url="https://www.plazajapan.com/pokemon-center-original/?sort=newest&page=1",
            callback=self.web1_prod_listings
            # url="https://www.plazajapan.com/4521329327402/",
            # callback=self.web1_prod_details
        )

    def web1_prod_listings(self, response):
        print(response.url)
        prodUrls = response.xpath("(//ul[contains(@class, 'productGrid')])[last()]/li[@class='product']//h4/a/@href").getall()
        for prodUrl in prodUrls:
            yield scrapy.Request(
                url=prodUrl,
                callback=self.web1_prod_details,
            )       

        #-- Handling Pagination --#
        nextPage = response.xpath("//a[contains(text(), 'Next')]/@href").get()
        if nextPage:
            yield scrapy.Request(
                url=nextPage,
                callback=self.web1_prod_listings
            )

    def web1_prod_details(self, response):
        upc = response.xpath("//dd[@data-product-upc]/text()").get()

        if response.xpath("//input[contains(@id, 'form-action-buyNow')]").get():
            yield scrapy.Request(
                url=f"https://www.pokemoncenter-online.com/?p_cd={upc}",
                callback=self.web2_stock_status,
                meta={
                    'upc': upc
                }            
            )

    def web2_stock_status(self, response):
        upc = response.request.meta['upc']
        if not response.xpath("//td/img[contains(@src, 'btn_cart.jpg')]").get():
            yield{
                'Upc': upc
            }