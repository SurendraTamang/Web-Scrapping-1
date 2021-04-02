import scrapy
import json
import pandas as pd
import csv
import os.path


class PartslistSpider(scrapy.Spider):
    name = 'partsList'

    # df = pd.read_excel("D:/Web-Scrapping/UpWork_Projects/kacper/customPartrefDotCom/inputData.xlsx",sheet_name='test')
    df = pd.read_excel("inputData.xlsx")

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
                # url=f'''http://custom.partref.com/AGR/Home/GetAdvanceSearchResult?Partno=106&SearchType=Begins+With&DescriptionID=&SpecValues=''',
                method='GET',
                cookies={
                    'ASP.NET_SessionId': 'xsino3jd14dltcoqt2iuell0',
                },
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36 Edg/86.0.622.51',
                    'X-Requested-With': 'XMLHttpRequest',
                    'Host': 'custom.partref.com',
                    'Referer': 'http://custom.partref.com/AGR',
                    'Accept': '*/*',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Connection': 'keep-alive',
                },
                callback=self.getPartID,
                meta={
                    'name': 'test'
                    # 'name': val['Name']
                }
            )

    def getPartID(self, response):
        json_resps = json.loads(response.body)

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
                        'interchange': json_resp.get('InterchangePartNo'),
                        'name': name,
                    }
                )

    def parse(self, response):
        interchangeData = []
        applicationData = []
        imgNameLi = []

        interchange = response.request.meta['interchange']
        imageLabel = None
        name = response.request.meta['name']

        for _,val in self.df.iterrows():
            if str(interchange) in str(val['Interchange']) or str(val['Interchange']) in str(interchange):
                imageLabel = val['Part Number to label images']
                imgNameLi.append(val['Part Number to label images'])

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
        circType = None
        design = None
        mbhq = None
        mountType = None
        pwrRating = None
        sdhp = None
        toothQty = None

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
            elif prodAtr.get('AttributeName') == 'Ground Type' or prodAtr.get('AttributeName') == 'Case Grounding':
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
            elif prodAtr.get('AttributeName') == 'Rotation Direction' or prodAtr.get('AttributeName') == 'Generator Rotation' or prodAtr.get('AttributeName') == 'Starter Rotation':
                rotDir = prodAtr.get('AttributValues')
            elif prodAtr.get('AttributeName') == 'Voltage':
                voltage = prodAtr.get('AttributValues')
            elif prodAtr.get('AttributeName') == 'Circuit Type':
                circType = prodAtr.get('AttributValues')
            elif prodAtr.get('AttributeName') == 'Design':
                design = prodAtr.get('AttributValues')
            elif prodAtr.get('AttributeName') == 'Mounting Bolt Hole Quantity':
                mbhq = prodAtr.get('AttributValues')
            elif prodAtr.get('AttributeName') == 'Mounting Type':
                mountType = prodAtr.get('AttributValues')
            elif prodAtr.get('AttributeName') == 'Power Rating':
                pwrRating = prodAtr.get('AttributValues')
            elif prodAtr.get('AttributeName') == 'Starter Drive Housing Position':
                sdhp = prodAtr.get('AttributValues')
            elif prodAtr.get('AttributeName') == 'Tooth Quantity':
                toothQty = prodAtr.get('AttributValues')
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
            'Circuit Type': circType,
            'Design': design,
            'Mounting Bolt Hole Quantity': mbhq,
            'Mounting Type': mountType,
            'Power Rating': pwrRating,
            'Starter Drive Housing Position': sdhp,
            'Tooth Quantity': toothQty,
            'Part Image Url': partImgUrl,
            'Plug Image Url': pImgUrl,
            'Image Name List': " , ".join(imgNameLi)
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
        
        self.writeCSV("interchangeData.csv", interchangeData, ["Interchange (Search Number)","Part Number to label images","Brand","Interchange Number"])
        self.writeCSV("applicationData.csv", applicationData, ["Interchange (Search Number)","Part Number to label images","Year","Make","Model","Engine"])
        
