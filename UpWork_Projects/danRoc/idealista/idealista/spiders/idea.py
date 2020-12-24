import scrapy


class IdeaSpider(scrapy.Spider):
    name = 'idea'
    
    def start_requests(self):
        yield scrapy.Request(
            url="https://www.idealista.com/venta-viviendas/a-coruna-a-coruna/",
            callback=self.getListings
        )

    def getListings(self, response):
        adLi = response.xpath("//section[@class='items-container']/article[contains(@class, 'item')]")
        for ad in adLi:
            image = ad.xpath(".//picture[contains(@class,'gallery')]/img/@data-ondemand-img").get()
            try:
                img = image.replace("WEB_LISTING","WEB_DETAIL_TOP")
            except:
                img = None
            if not ad.xpath("//picture[@class='logo-branding']"):
                yield scrapy.Request(
                    url=f'''https://www.idealista.com{ad.xpath(".//a[@role='heading']/@href").get()}''',
                    callback=self.parse,
                    meta={
                        'image': img
                    }
                )

    def parse(self, response):
        onrName = response.xpath("normalize-space(//span[@class='particular']/input/@value)").get()
        if onrName:
            addr_raw = response.xpath("//h2[text()='Ubicación']/following-sibling::ul/li/text()").getall()
            yield{
                'Property Title': response.xpath("normalize-space(//h1/span/text())").get(),
                'Area in meter sq': response.xpath("normalize-space(//h2[text()='Características básicas']/following-sibling::div/ul/li[contains(text(),'m²')]/text())").get(),
                'Bed': response.xpath("normalize-space(//h2[text()='Características básicas']/following-sibling::div/ul/li[contains(text(),'habit')]/text())").get(),
                'Bath': response.xpath("normalize-space(//h2[text()='Características básicas']/following-sibling::div/ul/li[contains(text(),'baño')]/text())").get(),
                'Price': response.xpath("normalize-space(//span[contains(@class, 'price')]/span/text())").get(),
                'Owner Name': onrName,
                'Phone': response.xpath("normalize-space(//p[contains(@class, 'Phone')]/text())").get(),
                'Reference No': response.xpath("normalize-space(//p[contains(text(), 'Anuncio')]/text())").get(),
                'Type': None,
                'Rent/Sale': None,
                'Address': " , ".join(addr.strip() for addr in addr_raw),
                'Images': response.request.meta['image'],
                'Image Main': response.xpath("//div[@class='main-image_first']/img/@src").get(),
                'Url': response.url
            }
