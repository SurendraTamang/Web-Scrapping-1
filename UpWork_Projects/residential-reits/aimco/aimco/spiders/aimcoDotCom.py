import scrapy


class AimcodotcomSpider(scrapy.Spider):
    name = 'aimcoDotCom'

    def start_requests(self):
        yield scrapy.Request(
            url="https://www.aimco.com/en/community.html",
            callback=self.getCityUrls
        )

    def getCityUrls(self, response):
        urls = response.xpath("//div[@class='row']/div[@data-city]")
        for url in urls:
            yield{
                'cityUrl': url.xpath(".//a[contains(@class, 'commName')]/@href").get(),
                'communityName': url.xpath("normalize-space(.//a[contains(@class, 'commName')]/text())").get(),
                'address': url.xpath("normalize-space(.//p[contains(@class, 'address')]/text())").get()
            }
            # yield scrapy.Request(
            #     url=f'''{url.xpath(".//a[contains(@class, 'commName')]/@href").get()}/en/apartments/residences.html''',
            #     callback=self.parse,
            #     meta={
            #         'cityUrl': url.xpath(".//a[contains(@class, 'commName')]/@href").get(),
            #         'address': url.xpath("normalize-space(.//p[contains(@class, 'address')]/text())").get()
            #     }
            # )

    def parse(self, response):
        cityUrl = response.request.meta['cityUrl']
        apartments = response.xpath("//div[contains(@class,'featuredView')]/a")
        for apartment in apartments:            
            #   MIN MAX PRICE   #
            minPrice = apartment.xpath(".//div/@data-minrent").get()
            maxPrice = apartment.xpath(".//div/@data-maxrent").get()
            if minPrice and maxPrice:
                price = f'''${min}-${max}'''
            elif minPrice and not maxPrice:
                price = minPrice
            elif maxPrice and not minPrice:
                price = maxPrice
            else:
                price = None
            #   MIN MAX PRICE ENDS   #

            floorPlanDtls = response.xpath("normalize-space(.//div[@class='floorplan-details']/h4/text())").get()
            floorPlanType = floorPlanDtls.strip(",")[0].strip()
            apartmentNo = floorPlanDtls.strip(",")[1].strip()

            yield{
                'apartment url': f'''{cityUrl}{apartment.xpath(".//@href").get()}''',
                'price': price,
                'floorPlanType': floorPlanType,
                'apartmentNo': apartmentNo,
                'availability': apartment.xpath("normalize-space(.//span[@class='available-now']/text())").get(),
                'area in sq ft': apartment.xpath(".//div[@class='floor_det']/p/span[contains(text(), 'sq')]/text()").get().replace("sq.ft","").strip(),
                'bed': apartment.xpath(".//div[@class='floor_det']/p/span[contains(text(), 'Beds')]/text()").get().replace("Beds","").strip(),
                'bath': apartment.xpath(".//div[@class='floor_det']/p/span[contains(text(), 'Baths')]/text()").get().replace("Beds","").strip(),
                'floorPlanImgUrl': f'''{cityUrl}{apartment.xpath(".//@href").get()}''',
                'cityUrl': cityUrl
            }

            # yield scrapy.Request(
            #     url=f'''{response.request.meta['cityUrl']}{apartment.xpath(".//@href").get()}''',
            #     callback=self.getApartmentDetails,
            #     meta={
            #         'price': price,
            #         'floorPlanImgUrl': f'''{response.request.meta['cityUrl']}{apartment.xpath(".//@href").get()}'''
            #     }
            # )
