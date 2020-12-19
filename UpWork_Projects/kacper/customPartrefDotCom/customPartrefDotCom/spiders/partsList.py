import scrapy
import json
import pandas as pd
import csv
import os.path


class PartslistSpider(scrapy.Spider):
    name = 'partsList'

    # df = pd.read_excel("D:/Web-Scrapping/UpWork_Projects/kacper/customPartrefDotCom/inputData.xlsx",sheet_name='test')
    df = pd.read_excel("/home/p.byom26/myWrkSpc/customPartrefDotCom/inputData.xlsx")

    def writeCSV(self, fileName, dict_data, fieldName):
        file_exists = os.path.isfile(fileName)
        with open(fileName, 'a', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldName, lineterminator='\n')
            if not file_exists:
                writer.writeheader()
            for data in dict_data:
                writer.writerow(data)
    
    def start_requests(self):
        for _,val in self.df.iterrows():
            yield scrapy.Request(
                url=f'''http://custom.partref.com/AGR/Home/GetAdvanceSearchResult?Partno={str(val['Interchange']).replace(" ","+").strip()}&SearchType=Begins+With&DescriptionID=&SpecValues=''',
                method='GET',
                cookies={
                    'ASP.NET_SessionId': 'tkof3jbzmmlcvc5hwc1wv4p4',
                },
                callback=self.getPartID,
                meta={
                    'name': val['Name'],
                    'interchange': val['Interchange'],
                    'imageLabel': val['Part Number to label images'],
                }
            )

    def getPartID(self, response):
        json_resps = json.loads(response.body)

        interchange = response.request.meta['interchange']
        imageLabel = response.request.meta['imageLabel']
        name = response.request.meta['name']

        for json_resp in json_resps:
            if json_resp.get('ApplicationList') and json_resp.get('InterchangeName')==name:
                yield scrapy.Request(
                    url=f'''http://custom.partref.com/AGR/Home/GetUnitDetails?UserID=2383&PartId={json_resp.get('partid')}&RegionID=2%2C3%2C1&UnitActionName=Unit''',
                    method='GET',
                    cookies={
                        'ASP.NET_SessionId': 'tkof3jbzmmlcvc5hwc1wv4p4',
                    },
                    callback=self.parse,
                    meta={
                        'interchange': interchange,
                        'imageLabel': imageLabel,
                        'name': name,
                    }
                )

    def parse(self, response):
        interchangeData = []
        applicationData = []

        interchange = response.request.meta['interchange']
        imageLabel = response.request.meta['imageLabel']
        name = response.request.meta['name']

        json_resps = json.loads(response.body)
        prodAtrs = json_resps.get('ProductAttributes')

        manufacture = None
        ampRating = None
        dcp = None
        fanType = None
        grndType = None
        pcrvmme = None
        plugType = None
        pulleyBeltType = None
        pulleyGvQty = None
        pulleyOsDia = None
        regType = None
        rotDir = None
        voltage = None

        plugImgLi = []
        plugImgs = json_resps.get('plugcode')
        for plugImg in plugImgs:
            plugImgLi.append(f'''https://youtech.apapmt.com/PartImages/YTH/plugcodeimages/{plugImg.get('plugcodeimg')}''')
        pImgUrl = ",".join(plugImgLi)

        partImgLi = []
        partImgs = json_resps.get('PartImages')
        for partImg in partImgs:
            partImgLi.append(f'''https://youtech.apapmt.com/PartImages/YTH/{partImg.get('AssetName')}''')
        partImgUrl = ",".join(partImgLi)

        for prodAtr in prodAtrs:
            if prodAtr.get('AttributeName') == 'Manufacture':
                manufacture = prodAtr.get('AttributValues')
            elif prodAtr.get('AttributeName') == 'Amperage Rating':
                ampRating = prodAtr.get('AttributValues')
            elif prodAtr.get('AttributeName') == 'Decoupled Or Clutch Pulley':
                dcp = prodAtr.get('AttributValues')
            elif prodAtr.get('AttributeName') == 'Fan Type':
                fanType = prodAtr.get('AttributValues')
            elif prodAtr.get('AttributeName') == 'Ground Type':
                grndType = prodAtr.get('AttributValues')
            elif prodAtr.get('AttributeName') == 'Plug Clock Rear View Main Mounting Ear at 6 O Clock':
                pcrvmme = prodAtr.get('AttributValues')
            elif prodAtr.get('AttributeName') == 'Plug Type':
                plugType = prodAtr.get('AttributValues')
            elif prodAtr.get('AttributeName') == 'Pulley Belt Type':
                pulleyBeltType = prodAtr.get('AttributValues')
            elif prodAtr.get('AttributeName') == 'Pulley Groove Quantity':
                pulleyGvQty = prodAtr.get('AttributValues')
            elif prodAtr.get('AttributeName') == 'Pulley Outside Diameter':
                pulleyOsDia = prodAtr.get('AttributValues')
            elif prodAtr.get('AttributeName') == 'Regulator Type':
                regType = prodAtr.get('AttributValues')
            elif prodAtr.get('AttributeName') == 'Rotation Direction':
                rotDir = prodAtr.get('AttributValues')
            elif prodAtr.get('AttributeName') == 'Voltage':
                voltage = prodAtr.get('AttributValues')
            else:
                pass

        yield {
            'Interchange (Search Number)': interchange,
            'Name': name,
            'Part Number to label images': imageLabel,
            'Manufacture': manufacture,
            'Amperage Rating': ampRating,
            'Decoupled Or Clutch Pulley': dcp,
            'Fan Type': fanType,
            'Ground Type': grndType,
            'Plug Clock Rear View Main Mounting Ear at 6 O Clock': pcrvmme,
            'Plug Type': plugType,
            'Pulley Belt Type': pulleyBeltType,
            'Pulley Groove Quantity': pulleyGvQty,
            'Pulley Outside Diameter': pulleyOsDia,
            'Regulator Type': regType,
            'Rotation Direction': rotDir,
            'Voltage': voltage,
            'Part Image Url': partImgUrl,
            'Plug Image Url': pImgUrl,
        }

        intrLi = json_resps.get('CompetitorDetails')
        for intr in intrLi:
            intrChngNum = intr.get('CompetitorPartNo').split(",")
            for intChng in intrChngNum:
                interchangeData.append(
                    {
                        'Interchange (Search Number)': interchange,
                        'Part Number to label images': imageLabel,
                        'Brand': intr.get('CompetitorName'),
                        'Interchange Number': intChng.strip()
                    }
                )
        
        appLi = json_resps.get('ApplicatioDetails')
        for app in appLi:
            applicationData.append(
                {
                    'Interchange (Search Number)': interchange,
                    'Part Number to label images': imageLabel,
                    'Year': f'''{app.get('FromYear')}-{app.get('ToYear')}''',
                    'Make': app.get('MakeName'),
                    'Model': app.get('ModelName'),
                    'Engine': app.get('Engine'),
                }
            )
        
        self.writeCSV("/home/p.byom26/myWrkSpc/customPartrefDotCom/interchangeData.csv", interchangeData, ["Interchange (Search Number)","Part Number to label images","Brand","Interchange Number"])
        self.writeCSV("/home/p.byom26/myWrkSpc/customPartrefDotCom/applicationData.csv", applicationData, ["Interchange (Search Number)","Part Number to label images","Year","Make","Model","Engine"])
        
