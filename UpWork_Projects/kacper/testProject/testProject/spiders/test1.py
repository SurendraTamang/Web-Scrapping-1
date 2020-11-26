import scrapy


class Test1Spider(scrapy.Spider):
    name = 'test1'
    
    def start_requests(self):
        yield scrapy.Request(
            url="https://www.avaloncommunities.com/california/woodland-hills-apartments/avalon-woodland-hills/apartments",
            callback=self.parse
        )

    def parse(self, response):
        apartments = response.xpath("//ul[contains(@class, 'apartment-cards')]/li")
        for apartment in apartments:
            apartmentNo = apartment.xpath("normalize-space(.//div[contains(@class, 'title')]/text())").get()
                
            if apartmentNo != "Unavailable":
                houseDetails =  apartment.xpath("normalize-space(.//div[contains(@class, 'details')]/text())").get()
                try:
                    bed = houseDetails.split("•")[-3].strip().split(" ")[0]
                except:
                    bed = None
                yield{
                    'Bed': bed,
                    'Bath': houseDetails.split("•")[-2].strip().split(" ")[0],
                    'Area in sq ft': houseDetails.split("•")[-1].strip().replace(" sqft", "")
                }