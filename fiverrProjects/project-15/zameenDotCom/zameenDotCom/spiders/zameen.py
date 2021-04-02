# import scrapy
# import json
# import os
# import csv


# class ZameenSpider(scrapy.Spider):
#     name = 'zameen'
#     BASE_DIR = "Lahore"
#     FIELD_NAMES = [
#         'Plot Area',
#         'Name',
#         'Number1',
#         'Number2',
#         'Company Name',
#         'Status',
#         'Ad Status',
#         'Property ID'
#     ]

#     def writeCSV(self, data, fieldName, file_name):
#         fileExists = os.path.isfile(file_name)
#         with open(file_name, 'a', encoding='utf-8') as csvfile:
#             writer = csv.DictWriter(csvfile, fieldnames=fieldName, lineterminator='\n')
#             if not fileExists:
#                 writer.writeheader()
#             writer.writerow(data)

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
#                 # if areaName.lower().startswith('a'):
#                 yield scrapy.Request(
#                     # url=f'''{li.xpath(".//a/@href").get()}?load_all_prop=1''',
#                     url=li.xpath(".//a/@href").get(),
#                     callback=self.getPropertyID,
#                     meta={
#                         'fileName': f'''{areaName}.csv'''
#                     }
#                 )

#     def getPropertyID(self, response):
#         fileName = response.request.meta['fileName']
#         plots = response.xpath("//div/ul/li[@role='article']")
#         for plot in plots:
#             isActive = plot.xpath(".//article/@class").get().split(" ")
#             if len(isActive) == 1:
#                 yield scrapy.Request(
#                     url=f'''https://www.zameen.com/nfpage/async/show-numbers?property_id={plot.xpath(".//a/@href").get().split("-")[1]}''',
#                     method="POST",
#                     headers={
#                         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36 Edg/89.0.774.50',
#                         'x-requested-with': 'XMLHttpRequest'
#                     },
#                     callback=self.parse,
#                     meta={
#                         'adStatus': plot.xpath("normalize-space(.//div[contains(@aria-label, 'label')]/text())").get(),
#                         'status': plot.xpath("normalize-space(.//span[contains(@aria-label, ' badge')]/text())").get(),
#                         'companyName': plot.xpath("normalize-space(.//div[contains(@aria-label, 'Location')]/text())").get(),
#                         'plotArea': plot.xpath("normalize-space(.//span[contains(@aria-label, 'Area')]//div/span/text())").get(),
#                         'propertyId': plot.xpath(".//a/@href").get().split("-")[1],
#                         'fileName': fileName
#                     }
#                 )
        
#         nextPage = response.xpath("//li/a[@title='Next']/@href").get()
#         if nextPage:
#             yield scrapy.Request(
#                 url=f'''https://www.zameen.com{nextPage}''',
#                 callback=self.getPropertyID,
#                 meta={
#                     'fileName': fileName
#                 }
#             )

#     def parse(self, response):
#         fileName = response.request.meta['fileName']
#         json_resp = json.loads(response.body)
#         try:
#             cp = json_resp.get('result').get('number').get('contact_person')
#         except:
#             cp = None
#         try:
#             mob = json_resp.get('result').get('number').get('mobile').replace("=","")
#             if len(mob) < 5:
#                 mob = None
#         except:
#             mob = None
#         try:
#             phone = json_resp.get('result').get('number').get('phone').replace("=","")
#             if len(phone) < 5:
#                 phone = None
#         except:
#             phone = None
#         dataDict = {
#             self.FIELD_NAMES[0]: response.request.meta['plotArea'],
#             self.FIELD_NAMES[1]: cp,
#             self.FIELD_NAMES[2]: f'''{mob}''',
#             self.FIELD_NAMES[3]: f'''{phone}''',
#             self.FIELD_NAMES[4]: response.request.meta['companyName'],
#             self.FIELD_NAMES[5]: response.request.meta['status'],
#             self.FIELD_NAMES[6]: response.request.meta['adStatus'],
#             self.FIELD_NAMES[7]: f'''{response.request.meta['propertyId']}''',
#         }
#         print(dataDict)
#         self.writeCSV(dataDict, self.FIELD_NAMES, f'''{self.BASE_DIR}/{fileName}''')
