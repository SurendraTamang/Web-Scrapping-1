import scrapy
import json
import os
import csv
import pandas as pd


class ZameenfullSpider(scrapy.Spider):
    name = 'zameenFull'

    propIDLi = []
    df = pd.read_excel("inputFiles/inputLinks.xlsx", sheet_name="large")
    BASE_DIR = "data/4_commercial/"
    FIELD_NAMES = [
        'Type',
        'Area',
        'Price',
        'Purpose',
        'Location',
        'Added',
        'Number1',
        'Number2',
        'Customer Name',
        'Company Name',
        'Ad Status',
        'Company Status',
        'Property ID',
        'Ad Link',
        'City Name',
        # 'Bedroom',
        # 'Bathroom'
    ]

    # try:
    #     with open(f'{BASE_DIR}house1.csv') as csv_file:
    #         csv_reader = csv.reader(csv_file, delimiter=',')
    #         for indx,data in enumerate(csv_reader):
    #             if indx != 0:
    #                 propIDLi.append(data[-5])
    # except:
    #     pass

    def writeCSV(self, data, fieldName, file_name):
        fileExists = os.path.isfile(file_name)
        with open(file_name, 'a', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldName, lineterminator='\n')
            if not fileExists:
                writer.writeheader()
            writer.writerow(data)

    def start_requests(self):
        for _,val in self.df.iterrows():
            yield scrapy.Request(
                url=val['url'],
                callback=self.getAllAreasUrl,
                # callback=self.getPropertyID,
                meta={
                    'fileName': f"link {val['slno']}"
                }
            )

    def getAllAreasUrl(self,response):
        viewAll = response.xpath("//a[contains(text(), 'View All Locations')]/@href").get()
        if viewAll:
            yield scrapy.Request(
                url=f'''https://www.zameen.com{viewAll}''',
                callback=self.getAreas,
                meta={
                    'fileName': response.request.meta['fileName']
                }
            )

    def getAreas(self, response):
        uls = response.xpath("//div[@id='sub-location-list']/ul")
        for url in uls:
            lis = url.xpath(".//li")
            for li in lis:
                # areaName = li.xpath("normalize-space(.//a/text())").get()
                # if areaName.lower().startswith('a'):
                yield scrapy.Request(
                    # url=f'''{li.xpath(".//a/@href").get()}?load_all_prop=1''',
                    url=li.xpath(".//a/@href").get(),
                    callback=self.getPropertyID,
                    meta={
                        'fileName': response.request.meta['fileName']
                    }
                )


    def getPropertyID(self, response):
        fileName = response.request.meta['fileName']
        plots = response.xpath("//div/ul/li[@role='article']")
        for plot in plots:
            isActive = plot.xpath(".//article/@class").get().split(" ")
            if len(isActive) == 1:
                adUrl = plot.xpath(".//a/@href").get()
                propID = adUrl.split("-")[1]
                if propID.isdigit() and propID not in self.propIDLi:
                    yield scrapy.Request(
                        url=f'''https://www.zameen.com{adUrl}''',
                        # method="POST",
                        # headers={
                        #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36 Edg/89.0.774.50',
                        #     'x-requested-with': 'XMLHttpRequest'
                        # },
                        callback=self.parse,
                        meta={
                            'adStatus': plot.xpath("normalize-space(.//div[contains(@aria-label, 'label')]/text())").get(),
                            'status': plot.xpath("normalize-space(.//span[contains(@aria-label, ' badge')]/text())").get(),
                            'companyName': plot.xpath("normalize-space(.//div[contains(@aria-label, 'Location')]/text())").get(),
                            'plotArea': plot.xpath("normalize-space(.//span[contains(@aria-label, 'Area')]//div/span/text())").get(),
                            'propertyId': propID,
                            'fileName': fileName
                        }
                    )
        
        nextPage = response.xpath("//li/a[@title='Next']/@href").get()
        if nextPage:
            yield scrapy.Request(
                url=f'''https://www.zameen.com{nextPage}''',
                callback=self.getPropertyID,
                meta={
                    'fileName': fileName
                }
            )

    # def contactAPI(self, response):
    #     json_resp = json.loads(response.body)
    #     try:
    #         cp = json_resp.get('result').get('number').get('contact_person')
    #     except:
    #         cp = None
    #     try:
    #         mob = json_resp.get('result').get('number').get('mobile').replace("=","")
    #         if len(mob) < 5:
    #             mob = None
    #     except:
    #         mob = None
    #     try:
    #         phone = json_resp.get('result').get('number').get('phone').replace("=","")
    #         if len(phone) < 5:
    #             phone = None
    #     except:
    #         phone = None

    #     yield scrapy.Request(
    #         url=response.request.meta['adUrl'],
    #         callback=self.parse,
    #         meta={
    #             'adStatus': response.request.meta['adStatus'],
    #             'companyStatus': response.request.meta['status'],
    #             'companyName': response.request.meta['companyName'],
    #             'plotArea': response.request.meta['plotArea'],
    #             'propertyId': response.request.meta['propertyId'],
    #             'custName': cp,
    #             'num1': mob,
    #             'num2': phone,
    #             'fileName': response.request.meta['fileName']                
    #         }
    #     )

    def parse(self, response):
        scriptData = response.xpath("normalize-space(//div[@id='body-wrapper']/following-sibling::script[1]/text())").get().encode("ascii", "ignore")
        string_decode = scriptData.decode().split("window.webpackBundles")[0].replace("window.state = ","")
        jsonObj = json.loads(string_decode.strip()[:-1].replace("\n",""))
        num1 = ",".join(i.strip() for i in jsonObj.get('property').get('data').get('phoneNumber').get('mobileNumbers') if i.strip())
        num2 = ",".join(i.strip() for i in jsonObj.get('property').get('data').get('phoneNumber').get('phoneNumbers') if i.strip())
        custName = jsonObj.get('property').get('data').get('contactName')

        fileName = response.request.meta['fileName']
        price = response.xpath("//ul/li/span[text()='Price']/following-sibling::span/div/text()").getall()        
        
        dataDict = {
            self.FIELD_NAMES[0]: response.xpath("normalize-space(//ul/li/span[text()='Type']/following-sibling::span/text())").get(),
            self.FIELD_NAMES[1]: response.request.meta['plotArea'],
            self.FIELD_NAMES[2]: " ".join(i.strip() for i in price if price),
            self.FIELD_NAMES[3]: response.xpath("normalize-space(//ul/li/span[text()='Purpose']/following-sibling::span/text())").get(),
            self.FIELD_NAMES[4]: response.xpath("normalize-space(//ul/li/span[text()='Location']/following-sibling::span/text())").get(),
            self.FIELD_NAMES[5]: response.xpath("normalize-space(//ul/li/span[text()='Added']/following-sibling::span/text())").get(),
            self.FIELD_NAMES[6]: num1,
            self.FIELD_NAMES[7]: num2,
            self.FIELD_NAMES[8]: custName,
            self.FIELD_NAMES[9]: response.xpath("normalize-space(//div[@aria-label='Agency info']/div/text())").get(),
            self.FIELD_NAMES[10]: response.request.meta['adStatus'],
            self.FIELD_NAMES[11]: response.request.meta['status'],
            self.FIELD_NAMES[12]: f'''{response.request.meta['propertyId']}''',
            self.FIELD_NAMES[13]: response.url,
            self.FIELD_NAMES[14]: fileName,
            # self.FIELD_NAMES[15]: response.xpath("normalize-space(//ul/li/span[contains(text(),'Bed')]/following-sibling::span/text())").get(),
            # self.FIELD_NAMES[16]: response.xpath("normalize-space(//ul/li/span[contains(text(),'Bath')]/following-sibling::span/text())").get(),
        }
        # print(dataDict)
        self.writeCSV(dataDict, self.FIELD_NAMES, f"{self.BASE_DIR}commercial.csv")