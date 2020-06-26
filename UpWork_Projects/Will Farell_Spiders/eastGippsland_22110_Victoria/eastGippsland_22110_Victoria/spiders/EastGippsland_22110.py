# -*- coding: utf-8 -*-
import scrapy


class Eastgippsland22110Spider(scrapy.Spider):
    name = 'EastGippsland_22110'
    
    def start_requests(self):
        yield scrapy.Request(
            url="https://www.eastgippsland.vic.gov.au/Planning_and_Building/Planning_Permits/Advertised_Planning_Permit_Applications",
            callback=self.parse
        )

    def parse(self, response):
        listings = response.xpath("//h3/following-sibling::p/a")

        for i in range(1, len(listings)+1):
            if i%2 != 0:
                line1 = response.xpath(f"(//h3/following-sibling::p/a/text())[{i}]").get()
            else:
                li = []               
                line2 = response.xpath(f"normalize-space((//h3/following-sibling::p/a/text())[{i}])").get()
                if line1:
                    li = line1.split("-")
                    li_len = len(li)
                    appNum1 = li[0].replace("Application", "") 
                    appNum2 = appNum1.replace("-", "")
                    address1 = li[li_len-1].replace("Application", "") 
                    address2 = address1.replace("-", "") 
                    yield{
                        'appNum': appNum2.strip(),
                        'nameLGA': 'EastGippsland',
                        'codeLGA': '21110',
                        'address': address2.strip(),
                        'activity': line2.strip("\xa0"),
                        'applicant': None,
                        'lodgeDate': None,
                        'decisionDate': None,
                        'status': None,
                        'url' : f'''https://www.eastgippsland.vic.gov.au{response.xpath(f"//h3/following-sibling::p/a[{i}]/@href").get()}''' 
                    }
                else:
                    pass

