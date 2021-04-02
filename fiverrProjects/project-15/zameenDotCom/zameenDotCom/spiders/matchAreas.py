# import scrapy
# import os


# class MatchareasSpider(scrapy.Spider):
#     name = 'matchAreas'
#     BASE_DIR = "Lahore"
#     _,_,files = next(os.walk('Lahore'))

#     def start_requests(self):
#         yield scrapy.Request(
#             url="https://www.zameen.com/all_locations/Lahore-1-1-2.html",
#             callback=self.getAreas
#         )

#     def getAreas(self, response):
#         uls = response.xpath("//div[@id='sub-location-list']/ul")
#         for url in uls:
#             lis = url.xpath(".//li")
#             for li in lis:
#                 areaName = li.xpath("normalize-space(.//a/text())").get()                
#                 if f'''{areaName}.csv''' not in self.files:
#                     print(areaName)

