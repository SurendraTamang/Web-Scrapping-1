import scrapy
import os
import csv
import json
from datetime import date, timedelta


class EstimatesurpriseSpider(scrapy.Spider):
    name = 'estimateSurprise'
    
    #API_TOKEN = os.environ.get('finnhubApiToken')
    API_TOKEN = "c0etd5n48v6p527umgtg"
    TODAY = date.today().strftime("%Y-%m-%d")
    SEVEN_DAYS_BACK = (date.today() - timedelta(days=7)).strftime("%Y-%m-%d")
    FIELD_NAMES = ['Symbol','priceTarget_lastUpdated','priceTarget_targetHigh','priceTarget_targetLow','priceTarget_targetMean','priceTarget_targetMedian','revenueEstimates_NumberAnalysts1','revenueEstimates_Period1','revenueEstimates_revenueAvg1','revenueEstimates_revenueHigh1','revenueEstimates_revenueLow1','revenueEstimates_NumberAnalysts2','revenueEstimates_Period2','revenueEstimates_revenueAvg2','revenueEstimates_revenueHigh2','revenueEstimates_revenueLow2','revenueEstimates_NumberAnalysts3','revenueEstimates_Period3','revenueEstimates_revenueAvg3','revenueEstimates_revenueHigh3','revenueEstimates_revenueLow3','revenueEstimates_NumberAnalysts4','revenueEstimates_Period4','revenueEstimates_revenueAvg4','revenueEstimates_revenueHigh4','revenueEstimates_revenueLow4','earningsEstimates_epsAvg1','earningsEstimates_epsHigh1','earningsEstimates_epsLow1','earningsEstimates_NumberAnalysts1','earningsEstimates_Period1','earningsEstimates_epsAvg2','earningsEstimates_epsHigh2','earningsEstimates_epsLow2','earningsEstimates_NumberAnalysts2','earningsEstimates_Period2','earningsEstimates_epsAvg3','earningsEstimates_epsHigh3','earningsEstimates_epsLow3','earningsEstimates_NumberAnalysts3','earningsEstimates_Period3','earningsEstimates_epsAvg4','earningsEstimates_epsHigh4','earningsEstimates_epsLow4','earningsEstimates_NumberAnalysts4','earningsEstimates_Period4','earningsSurprises_actual1','earningsSurprises_estimate1','earningsSurprises_period1','earningsSurprises_actual2','earningsSurprises_estimate2','earningsSurprises_period2','earningsSurprises_actual3','earningsSurprises_estimate3','earningsSurprises_period3','earningsSurprises_actual4','earningsSurprises_estimate4','earningsSurprises_period4']

    def writeCSV(self, data, fieldName, file_name):
        fileExists = os.path.isfile(file_name)
        with open(file_name, 'a', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldName, lineterminator='\n')
            if not fileExists:
                writer.writeheader()
            writer.writerow(data)

    #--Price Target--#
    def start_requests(self):
        _, _, files = next(os.walk("../earningsCalendar/data"))
        for file in files:
            symbol_list = []
            with open(f'../earningsCalendar/data/{file}') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for indx,symb in enumerate(csv_reader):
                    if indx != 0:
                        symbol_list.append(symb[0])
            for symb in symbol_list:
                dataDict = {}
                dataDict['Symbol'] = symb            
                yield scrapy.Request(
                    url=f"https://finnhub.io/api/v1/stock/price-target?symbol={symb}&token={self.API_TOKEN}",                
                    callback=self.revenueEstimates,
                    meta={
                        'dataDict': dataDict,
                        'fileName': file
                    }
                )

    #--Revenue Estimates--#
    def revenueEstimates(self, response):
        dataDict = response.request.meta['dataDict']
        json_resp = json.loads(response.body)

        try: dataDict['priceTarget_lastUpdated'] = json_resp.get('lastUpdated')
        except: dataDict['priceTarget_lastUpdated'] = None
        try: dataDict['priceTarget_targetHigh'] = json_resp.get('targetHigh')
        except: dataDict['priceTarget_targetHigh'] = None
        try: dataDict['priceTarget_targetLow'] = json_resp.get('targetLow')
        except: dataDict['priceTarget_targetLow'] = None
        try: dataDict['priceTarget_targetMean'] = json_resp.get('targetMean')
        except: dataDict['priceTarget_targetMean'] = None
        try: dataDict['priceTarget_targetMedian'] = json_resp.get('targetMedian')
        except: dataDict['priceTarget_targetMedian'] = None
        
        yield scrapy.Request(
            url=f"https://finnhub.io/api/v1/stock/revenue-estimate?symbol={dataDict['Symbol']}&freq=quarterly&token={self.API_TOKEN}",                
            callback=self.earningsEstimates,
            meta={
                'dataDict': dataDict,
                'fileName': response.request.meta['fileName']
            }
        )

    #--Earnings Estimates--#
    def earningsEstimates(self, response):
        dataDict = response.request.meta['dataDict']
        json_resp = json.loads(response.body)

        for i in range(1,5):
            try: dataDict[f'revenueEstimates_NumberAnalysts{i}'] = json_resp.get('data')[i-1].get('numberAnalysts')
            except: dataDict[f'revenueEstimates_NumberAnalysts{i}'] = None
            try: dataDict[f'revenueEstimates_Period{i}'] = json_resp.get('data')[i-1].get('period')
            except: dataDict[f'revenueEstimates_Period{i}'] = None
            try: dataDict[f'revenueEstimates_revenueAvg{i}'] = json_resp.get('data')[i-1].get('revenueAvg')
            except: dataDict[f'revenueEstimates_revenueAvg{i}'] = None
            try: dataDict[f'revenueEstimates_revenueHigh{i}'] = json_resp.get('data')[i-1].get('revenueHigh')
            except: dataDict[f'revenueEstimates_revenueHigh{i}'] = None
            try: dataDict[f'revenueEstimates_revenueLow{i}'] = json_resp.get('data')[i-1].get('revenueLow')
            except: dataDict[f'revenueEstimates_revenueLow{i}'] = None

        yield scrapy.Request(
            url=f"https://finnhub.io/api/v1/stock/eps-estimate?symbol={dataDict['Symbol']}&freq=quarterly&token={self.API_TOKEN}",                
            callback=self.earningsSurprises,
            meta={
                'dataDict': dataDict,
                'fileName': response.request.meta['fileName']
            }
        )

    #--Earnings Surprises--#
    def earningsSurprises(self, response):
        dataDict = response.request.meta['dataDict']
        json_resp = json.loads(response.body)

        for i in range(1,5):            
            try: dataDict[f'earningsEstimates_epsAvg{i}'] = json_resp.get('data')[i-1].get('epsAvg')
            except: dataDict[f'earningsEstimates_epsAvg{i}'] = None
            try: dataDict[f'earningsEstimates_epsHigh{i}'] = json_resp.get('data')[i-1].get('epsHigh')
            except: dataDict[f'earningsEstimates_epsHigh{i}'] = None
            try: dataDict[f'earningsEstimates_epsLow{i}'] = json_resp.get('data')[i-1].get('epsLow')
            except: dataDict[f'earningsEstimates_epsLow{i}'] = None
            try: dataDict[f'earningsEstimates_NumberAnalysts{i}'] = json_resp.get('data')[i-1].get('numberAnalysts')
            except: dataDict[f'earningsEstimates_NumberAnalysts{i}'] = None
            try: dataDict[f'earningsEstimates_Period{i}'] = json_resp.get('data')[i-1].get('period')
            except: dataDict[f'earningsEstimates_Period{i}'] = None

        yield scrapy.Request(
            url=f"https://finnhub.io/api/v1/stock/earnings?symbol={dataDict['Symbol']}&token={self.API_TOKEN}",                
            callback=self.parse,
            meta={
                'dataDict': dataDict,
                'fileName': response.request.meta['fileName']
            }
        )

    #--Parse menthod to generate the final output--#
    def parse(self, response):
        fileName = response.request.meta['fileName']
        dataDict = response.request.meta['dataDict']
        json_resp = json.loads(response.body)

        for i in range(1,5):            
            try: dataDict[f'earningsSurprises_actual{i}'] = json_resp[i-1].get('actual')
            except: dataDict[f'earningsSurprises_actual{i}'] = None
            try: dataDict[f'earningsSurprises_estimate{i}'] = json_resp[i-1].get('estimate')
            except: dataDict[f'earningsSurprises_estimate{i}'] = None
            try: dataDict[f'earningsSurprises_period{i}'] = json_resp[i-1].get('period')
            except: dataDict[f'earningsSurprises_period{i}'] = None

        print(dataDict)
        self.writeCSV(dataDict, self.FIELD_NAMES, f'data/{fileName.replace("symbols","data")}')
