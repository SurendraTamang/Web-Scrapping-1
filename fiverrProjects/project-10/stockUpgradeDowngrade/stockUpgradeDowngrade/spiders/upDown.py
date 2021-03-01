import scrapy
import os
import csv
import json
from datetime import datetime


class UpdownSpider(scrapy.Spider):
    name = 'upDown'
    
    API_TOKEN = "c0etd5n48v6p527umgtg"
    FROM = input("Enter FROM date in YYYY-MM-DD format: ")
    TO = input("Enter TO date in YYYY-MM-DD format: ")
    FIELD_NAMES = ['Symbol', 'GradeTime', 'Company', 'FromGrade', 'ToGrade', 'Action', 'Timestamp']
    FILE_NAME = f'''data/data_{datetime.now().strftime("%d-%m-%Y_%H-%M")}.csv'''

    def writeCSV(self, data, fieldName, file_name):
        fileExists = os.path.isfile(file_name)
        with open(file_name, 'a', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldName, lineterminator='\n')
            if not fileExists:
                writer.writeheader()
            writer.writerow(data)

    def start_requests(self):
        yield scrapy.Request(
            url=f"https://finnhub.io/api/v1/stock/upgrade-downgrade?from={self.FROM}&to={self.TO}&token={self.API_TOKEN}",
            callback=self.parse
        )

    def parse(self, response):
        symbol_list = []
        _, _, files = next(os.walk("data"))
        for file in files:
            with open(f'data/{file}') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for indx,symb in enumerate(csv_reader):
                    if indx != 0:
                        symbol_list.append(f"{symb[0]}_{symb[2]}")

        jsonResp = json.loads(response.body)
        for resp in jsonResp:
            dataDict = {}
            if f'''{resp.get('symbol')}_{resp.get('company')}''' not in symbol_list:
                dataDict['Symbol'] = resp.get('symbol')
                dataDict['GradeTime'] = resp.get('gradeTime')
                dataDict['Company'] = resp.get('company')
                dataDict['FromGrade'] = resp.get('fromGrade')
                dataDict['ToGrade'] = resp.get('toGrade')
                dataDict['Action'] = resp.get('action')
                # dataDict['Timestamp'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

                print(dataDict)
                self.writeCSV(dataDict, self.FIELD_NAMES, self.FILE_NAME)
