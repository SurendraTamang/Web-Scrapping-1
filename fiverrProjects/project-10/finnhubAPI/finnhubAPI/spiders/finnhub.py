import scrapy
import os
import csv
import json
from datetime import date, timedelta, datetime


class FinnhubSpider(scrapy.Spider):
    name = 'finnhub'

    symbol_list = []
    API_TOKEN = os.environ.get('finnhubApiToken')
    #API_TOKEN = "Place your token here"
    TODAY = date.today().strftime("%Y-%m-%d")
    SEVEN_DAYS_BACK = (date.today() - timedelta(days=7)).strftime("%Y-%m-%d")
    VARIATIONS = ['company-news', 'news-sentiment', 'recommendation-trends', 'company-basic-financials', 'aggregate-indicator']
    OP_FILE_GEN_TIME = datetime.now().strftime("%d-%m-%Y_%H-%M")

    # with open('symbolsData.csv') as csv_file:
    #     csv_reader = csv.reader(csv_file, delimiter=',')
    #     for symb in csv_reader:
    #         if symb[0] != "symbol":
    #             symbol_list.append(symb[0])

    def checkNone(self, data):
        if data:
            return data
        else:
            return None

    def writeCSV(self, data, fieldName, file_name):
        fileExists = os.path.isfile(file_name)
        with open(file_name, 'a', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldName, lineterminator='\n')
            if not fileExists:
                writer.writeheader()
            writer.writerow(data)

    def start_requests(self):
        for variation in self.VARIATIONS:
            for symb in self.symbol_list:
                if variation == "company-basic-financials":
                    yield scrapy.Request(
                        url=f"https://finnhub.io/api/v1/stock/metric?symbol={symb}&metric=all&from={self.SEVEN_DAYS_BACK}&to={self.TODAY}&token={self.API_TOKEN}",
                        callback=self.parse,
                        meta={'variation': variation}
                    )
                elif variation == "aggregate-indicator":
                    res = ['D', 'W', 'M']
                    for r in res:
                        yield scrapy.Request(
                            url=f'''https://finnhub.io/api/v1/scan/technical-indicator?symbol={symb}&resolution={r}&token={self.API_TOKEN}''',
                            callback=self.parse,
                            meta={'variation': variation, 'resolution': r, 'symbol': symb}
                        )
                elif variation == "recommendation-trends":
                    yield scrapy.Request(
                        url=f"https://finnhub.io/api/v1/stock/recommendation?symbol={symb}&from={self.SEVEN_DAYS_BACK}&to={self.TODAY}&token={self.API_TOKEN}",
                        callback=self.parse,
                        meta={'variation': variation}
                    )
                else:
                    yield scrapy.Request(
                        url=f"https://finnhub.io/api/v1/{variation}?symbol={symb}&from={self.SEVEN_DAYS_BACK}&to={self.TODAY}&token={self.API_TOKEN}",
                        callback=self.parse,
                        meta={'variation': variation}
                    )

    def parse(self, response):
        
        if response.request.meta['variation'] == "company-news":
            dataDict = {}
            fieldNames = []
            json_resp = json.loads(response.body)
            if json_resp:
                for i in range(1,4):
                    fieldNames += [f'Source{i}', f'Headline{i}', f'Related{i}', f'Url{i}']
                    dataDict[f'Source{i}'] = self.checkNone(json_resp[i-1].get('source'))
                    dataDict[f'Headline{i}'] = self.checkNone(json_resp[i-1].get('headline'))
                    dataDict[f'Related{i}'] = self.checkNone(json_resp[i-1].get('related'))
                    dataDict[f'Url{i}'] = self.checkNone(json_resp[i-1].get('url'))
                    #   ----    UN-COMMENT THE BELOW LINE WHILE USING ON YOUR LOCAL SYSTEM  ---- #
                    #print(dataDict)
                    self.writeCSV(dataDict, fieldNames, f'''data/companyNews_{self.OP_FILE_GEN_TIME}.csv''')
                    #   ----   UN-COMMENT THE BELOW LINE WHILE USING ON GOOGLE COLAB  ----  #
                    #self.writeCSV(dataDict, ['Source', 'Headline', 'Related', 'Url'], f'''/content/drive/MyDrive/finnhubAPI/data/companyNews_{self.OP_FILE_GEN_TIME}.csv''')
        
        elif response.request.meta['variation'] == "news-sentiment":
            json_resp = json.loads(response.body)
            if json_resp:
                dataDict = {
                    'Symbol': self.checkNone(json_resp.get('symbol')),
                    'ArticlesInLastWeek': self.checkNone(json_resp.get('buzz').get('articlesInLastWeek')),
                    'Buzz': self.checkNone(json_resp.get('buzz').get('buzz')),
                    'WeeklyAverage': self.checkNone(json_resp.get('buzz').get('weeklyAverage')),
                    'CompanyNewsScore': self.checkNone(json_resp.get('companyNewsScore')),
                    'SectorAverageBullishPercent': self.checkNone(json_resp.get('sectorAverageBullishPercent')),
                    'SectorAverageNewsScore': self.checkNone(json_resp.get('sectorAverageNewsScore')),
                    'BearishPercent': self.checkNone(json_resp.get('sentiment').get('bearishPercent')),
                    'BullishPercent': self.checkNone(json_resp.get('sentiment').get('bullishPercent')),
                    
                }
                #print(dataDict)
                #   ----    UN-COMMENT THE BELOW LINE WHILE USING ON YOUR LOCAL SYSTEM  ---- #
                self.writeCSV(dataDict, ['Symbol', 'ArticlesInLastWeek', 'Buzz', 'WeeklyAverage', 'CompanyNewsScore', 'SectorAverageBullishPercent', 'SectorAverageNewsScore', 'BearishPercent', 'BullishPercent'], f'''data/newsSentiment_{self.OP_FILE_GEN_TIME}.csv''')
                #   ----   UN-COMMENT THE BELOW LINE WHILE USING ON GOOGLE COLAB  ----  #
                #self.writeCSV(dataDict, ['Symbol', 'ArticlesInLastWeek', 'Buzz', 'WeeklyAverage', 'CompanyNewsScore', 'SectorAverageBullishPercent', 'SectorAverageNewsScore', 'BearishPercent', 'BullishPercent'], f'''/content/drive/MyDrive/finnhubAPI/data/newsSentiment_{self.OP_FILE_GEN_TIME}.csv''')
        
        elif response.request.meta['variation'] == "recommendation-trends":
            json_resp = json.loads(response.body)
            fieldNames = ['Symbol', 'Buy', 'Hold', 'Period', 'Sell', 'StrongBuy', 'StrongSell']
            if json_resp:
                dataDict = {
                        'Symbol': self.checkNone(json_resp[0].get('symbol')),
                        'Buy': self.checkNone(json_resp[0].get('buy')),
                        'Hold': self.checkNone(json_resp[0].get('hold')),
                        'Period': self.checkNone(json_resp[0].get('period')),
                        'Sell': self.checkNone(json_resp[0].get('sell')),
                        'StrongBuy': self.checkNone(json_resp[0].get('strongBuy')),
                        'StrongSell': self.checkNone(json_resp[0].get('strongSell')),
                    }
                indx = [1,3,6]
                for idx,val in enumerate(indx,1):
                    fieldNames += [f'Symbol{idx}', f'Buy{idx}', f'Hold{idx}', f'Period{idx}', f'Sell{idx}', f'StrongBuy{idx}', f'StrongSell{idx}']
                    dataDict[f'Symbol{idx}'] = self.checkNone(json_resp[val].get('symbol'))
                    dataDict[f'Buy{idx}'] = self.checkNone(json_resp[val].get('buy'))
                    dataDict[f'Hold{idx}'] = self.checkNone(json_resp[val].get('hold'))
                    dataDict[f'Period{idx}'] = self.checkNone(json_resp[val].get('period'))
                    dataDict[f'Sell{idx}'] = self.checkNone(json_resp[val].get('sell'))
                    dataDict[f'StrongBuy{idx}'] = self.checkNone(json_resp[val].get('strongBuy'))
                    dataDict[f'StrongSell{idx}'] = self.checkNone(json_resp[val].get('strongSell'))
                    
                #print(dataDict)
                #   ----    UN-COMMENT THE BELOW LINE WHILE USING ON YOUR LOCAL SYSTEM  ---- #
                self.writeCSV(dataDict, fieldNames, f'''data/recommendationTrends_{self.OP_FILE_GEN_TIME}.csv''')
                #   ----   UN-COMMENT THE BELOW LINE WHILE USING ON GOOGLE COLAB  ----  #
                #self.writeCSV(dataDict, ['Symbol', 'Buy', 'Hold', 'Period', 'Sell', 'StrongBuy', 'StrongSell'], f'''/content/drive/MyDrive/finnhubAPI/data/recommendationTrends_{self.OP_FILE_GEN_TIME}.csv''')
        
        elif response.request.meta['variation'] == "company-basic-financials":
            json_resp = json.loads(response.body)
            if json_resp:
                dataDict = {
                    'Symbol': self.checkNone(json_resp.get('symbol')),
                    '10DayAverageTradingVolume': self.checkNone(json_resp.get('metric').get('10DayAverageTradingVolume')),
                    '52WeekHigh': self.checkNone(json_resp.get('metric').get('52WeekHigh')),
                    '52WeekLow': self.checkNone(json_resp.get('metric').get('52WeekLow')),
                    '52WeekLowDate': self.checkNone(json_resp.get('metric').get('52WeekLowDate')),
                    '52WeekPriceReturnDaily': self.checkNone(json_resp.get('metric').get('52WeekPriceReturnDaily')),
                    'Beta': self.checkNone(json_resp.get('metric').get('beta'))           
                }
                #print(dataDict)
                #   ----    UN-COMMENT THE BELOW LINE WHILE USING ON YOUR LOCAL SYSTEM  ---- #
                self.writeCSV(dataDict, ['Symbol', '10DayAverageTradingVolume', '52WeekHigh', '52WeekLow', '52WeekLowDate', '52WeekPriceReturnDaily', 'Beta'], f'''data/companyBasicFinancials_{self.OP_FILE_GEN_TIME}.csv''')
                #   ----   UN-COMMENT THE BELOW LINE WHILE USING ON GOOGLE COLAB  ----  #
                #self.writeCSV(dataDict, ['Symbol', '10DayAverageTradingVolume', '52WeekHigh', '52WeekLow', '52WeekLowDate', '52WeekPriceReturnDaily', 'Beta'], f'''/content/drive/MyDrive/finnhubAPI/data/companyBasicFinancials_{self.OP_FILE_GEN_TIME}.csv''')
        
        elif response.request.meta['variation'] == "aggregate-indicator":
            json_resp = json.loads(response.body)
            resolution = response.request.meta['resolution']

            if resolution == "D":
                fieldNames = ['Symbol', 'TA_Daily_Buy', 'TA_Daly_Neutral', 'TA_Daily_Sell', 'TA_Daily_Signal', 'TA_Daily_ADX', 'TA_Daily_trending']
                fileName = f'''data/aggregateIndicatorsDaily_{self.OP_FILE_GEN_TIME}.csv'''
                #   ----   UN-COMMENT THE BELOW LINE WHILE USING ON GOOGLE COLAB  ----  #
                #fileName = f'''/content/drive/MyDrive/finnhubAPI/data/aggregateIndicatorsDaily_{self.OP_FILE_GEN_TIME}.csv'''
            if resolution == "W":
                fieldNames = ['Symbol', 'TA_Weekly_Buy', 'TA_Daly_Neutral', 'TA_Weekly_Sell', 'TA_Weekly_Signal', 'TA_Weekly_ADX', 'TA_Weekly_trending']
                #   ----    UN-COMMENT THE BELOW LINE WHILE USING ON YOUR LOCAL SYSTEM  ---- #
                fileName = f'''data/aggregateIndicatorsWeekly_{self.OP_FILE_GEN_TIME}.csv'''
                #   ----   UN-COMMENT THE BELOW LINE WHILE USING ON GOOGLE COLAB  ----  #
                #fileName = f'''/content/drive/MyDrive/finnhubAPI/data/aggregateIndicatorsWeekly_{self.OP_FILE_GEN_TIME}.csv'''
            if resolution == "M":
                fieldNames = ['Symbol', 'TA_Monthly_Buy', 'TA_Daly_Neutral', 'TA_Monthly_Sell', 'TA_Monthly_Signal', 'TA_Monthly_ADX', 'TA_Monthly_trending']
                #   ----    UN-COMMENT THE BELOW LINE WHILE USING ON YOUR LOCAL SYSTEM  ---- #
                fileName = f'''data/aggregateIndicatorsMonthly_{self.OP_FILE_GEN_TIME}.csv'''
                #   ----   UN-COMMENT THE BELOW LINE WHILE USING ON GOOGLE COLAB  ----  #
                #fileName = f'''/content/drive/MyDrive/finnhubAPI/data/aggregateIndicatorsMonthly_{self.OP_FILE_GEN_TIME}.csv'''

            if json_resp:
                dataDict = {
                    fieldNames[0]: response.request.meta['symbol'],
                    fieldNames[1]: self.checkNone(json_resp.get('technicalAnalysis').get('count').get('buy')),
                    fieldNames[2]: self.checkNone(json_resp.get('technicalAnalysis').get('count').get('neutral')),
                    fieldNames[3]: self.checkNone(json_resp.get('technicalAnalysis').get('count').get('sell')),
                    fieldNames[4]: self.checkNone(json_resp.get('technicalAnalysis').get('signal')),
                    fieldNames[5]: self.checkNone(json_resp.get('trend').get('adx')),
                    fieldNames[6]: self.checkNone(json_resp.get('trend').get('trending')),
                }
                #print(dataDict)
                self.writeCSV(dataDict, fieldNames, fileName)
        
        else:
            pass
