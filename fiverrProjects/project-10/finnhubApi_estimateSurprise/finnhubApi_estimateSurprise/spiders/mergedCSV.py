import scrapy
import os
import csv
import json
from datetime import date, timedelta


class MergedcsvSpider(scrapy.Spider):
    name = 'mergedCSV'
    
    symbol_list = []
    #API_TOKEN = os.environ.get('finnhubApiToken')
    API_TOKEN_FREE = "c0r6vsn48v6qllqsej60"
    API_TOKEN_PAID = "c0etd5n48v6p527umgtg"
    TODAY = date.today().strftime("%Y-%m-%d")
    SEVEN_DAYS_BACK = (date.today() - timedelta(days=7)).strftime("%Y-%m-%d")

    # with open('symbolsData.csv') as csv_file:
    #     csv_reader = csv.reader(csv_file, delimiter=',')
    #     for symb in csv_reader:
    #         if symb[0] != "symbol":
    #             symbol_list.append(symb[0])

    def writeCSV(self, data, fieldName, file_name):
        fileExists = os.path.isfile(file_name)
        with open(file_name, 'a', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldName, lineterminator='\n')
            if not fileExists:
                writer.writeheader()
            writer.writerow(data)

    def start_requests(self):
        _, _, files = next(os.walk("../earningsCalendar/data"))
        for file in files:
            field_names = ['Symbol','companyNews_Source1','companyNews_Headline1','companyNews_Url1','companyNews_Source2','companyNews_Headline2','companyNews_Url2','companyNews_Source3','companyNews_Headline3','companyNews_Url3','newsSentiment_ArticlesInLastWeek','newsSentiment_Buzz','newsSentiment_WeeklyAverage','newsSentiment_CompanyNewsScore','newsSentiment_SectorAverageBullishPercent','newsSentiment_SectorAverageNewsScore','newsSentiment_BearishPercent','newsSentiment_BullishPercent','recommendationTrends_Buy','recommendationTrends_Hold','recommendationTrends_Period','recommendationTrends_Sell','recommendationTrends_StrongBuy','recommendationTrends_StrongSell','recommendationTrends_Buy1','recommendationTrends_Hold1','recommendationTrends_Period1','recommendationTrends_Sell1','recommendationTrends_StrongBuy1','recommendationTrends_StrongSell1','recommendationTrends_Buy2','recommendationTrends_Hold2','recommendationTrends_Period2','recommendationTrends_Sell2','recommendationTrends_StrongBuy2','recommendationTrends_StrongSell2','recommendationTrends_Buy3','recommendationTrends_Hold3','recommendationTrends_Period3','recommendationTrends_Sell3','recommendationTrends_StrongBuy3','recommendationTrends_StrongSell3','companyBasicFinancials_10DayAverageTradingVolume','companyBasicFinancials_52WeekHigh','companyBasicFinancials_52WeekLow','companyBasicFinancials_52WeekLowDate','companyBasicFinancials_52WeekPriceReturnDaily','TA_Daily_Buy','TA_Daily_Neutral','TA_Daily_Sell','TA_Daily_Signal','TA_Daily_ADX','TA_Daily_trending','TA_Weekly_Buy','TA_Weekly_Neutral','TA_Weekly_Sell','TA_Weekly_Signal','TA_Weekly_ADX','TA_Weekly_trending','TA_Monthly_Buy','TA_Monthly_Neutral','TA_Monthly_Sell','TA_Monthly_Signal','TA_Monthly_ADX','TA_Monthly_trending','priceTarget_lastUpdated','priceTarget_targetHigh','priceTarget_targetLow','priceTarget_targetMean','priceTarget_targetMedian','revenueEstimates_NumberAnalysts1','revenueEstimates_Period1','revenueEstimates_revenueAvg1','revenueEstimates_revenueHigh1','revenueEstimates_revenueLow1','revenueEstimates_NumberAnalysts2','revenueEstimates_Period2','revenueEstimates_revenueAvg2','revenueEstimates_revenueHigh2','revenueEstimates_revenueLow2','revenueEstimates_NumberAnalysts3','revenueEstimates_Period3','revenueEstimates_revenueAvg3','revenueEstimates_revenueHigh3','revenueEstimates_revenueLow3','revenueEstimates_NumberAnalysts4','revenueEstimates_Period4','revenueEstimates_revenueAvg4','revenueEstimates_revenueHigh4','revenueEstimates_revenueLow4','earningsEstimates_epsAvg1','earningsEstimates_epsHigh1','earningsEstimates_epsLow1','earningsEstimates_NumberAnalysts1','earningsEstimates_Period1','earningsEstimates_epsAvg2','earningsEstimates_epsHigh2','earningsEstimates_epsLow2','earningsEstimates_NumberAnalysts2','earningsEstimates_Period2','earningsEstimates_epsAvg3','earningsEstimates_epsHigh3','earningsEstimates_epsLow3','earningsEstimates_NumberAnalysts3','earningsEstimates_Period3','earningsEstimates_epsAvg4','earningsEstimates_epsHigh4','earningsEstimates_epsLow4','earningsEstimates_NumberAnalysts4','earningsEstimates_Period4','earningsSurprises_actual1','earningsSurprises_estimate1','earningsSurprises_period1','earningsSurprises_actual2','earningsSurprises_estimate2','earningsSurprises_period2','earningsSurprises_actual3','earningsSurprises_estimate3','earningsSurprises_period3','earningsSurprises_actual4','earningsSurprises_estimate4','earningsSurprises_period4']
            # symbol_list = []
            with open(f'../earningsCalendar/data/{file}') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for indx,symb in enumerate(csv_reader):
                    if indx == 0:
                        for i,fname in enumerate(symb[1:],1):
                            field_names.insert(i, fname)
                    if indx != 0:
                        dataDict = {}
                        # dataDict['Symbol'] = symb[0]
                        for j,data in enumerate(symb,0):
                            dataDict[field_names[j]] = data

                        yield scrapy.Request(
                            url=f"https://finnhub.io/api/v1/company-news?symbol={dataDict['Symbol']}&from={self.SEVEN_DAYS_BACK}&to={self.TODAY}&token={self.API_TOKEN_FREE}",
                            callback=self.companyNews,
                            meta={
                                'dataDict': dataDict,
                                'fileName': file
                            }
                        )

    def companyNews(self, response):
        dataDict = response.request.meta['dataDict']
        json_resp = json.loads(response.body)

        for i in range(1,4):
            try:dataDict[f'companyNews_Source{i}'] = json_resp[i-1].get('source')
            except:dataDict[f'companyNews_Source{i}'] = None            
            try:dataDict[f'companyNews_Headline{i}'] = json_resp[i-1].get('headline')
            except:dataDict[f'companyNews_Headline{i}'] = None
            # try:dataDict[f'companyNews_Related{i}'] = json_resp[i-1].get('related')
            # except:dataDict[f'companyNews_Related{i}'] = None
            try:dataDict[f'companyNews_Url{i}'] = json_resp[i-1].get('url')
            except:dataDict[f'companyNews_Url{i}'] = None

        yield scrapy.Request(
            url=f"https://finnhub.io/api/v1/news-sentiment?symbol={dataDict['Symbol']}&from={self.SEVEN_DAYS_BACK}&to={self.TODAY}&token={self.API_TOKEN_FREE}",
            callback=self.newsSentiment,
            meta={
                'dataDict': dataDict,
                'fileName': response.request.meta['fileName']
            }
        )

    def newsSentiment(self, response):
        dataDict = response.request.meta['dataDict']
        json_resp = json.loads(response.body)
        
        #dataDict['Symbol'] = json_resp.get('symbol'))
        try: dataDict['newsSentiment_ArticlesInLastWeek'] = json_resp.get('buzz').get('articlesInLastWeek')
        except: dataDict['newsSentiment_ArticlesInLastWeek'] = None
        try: dataDict['newsSentiment_Buzz'] = json_resp.get('buzz').get('buzz')
        except: dataDict['newsSentiment_Buzz'] = None
        try: dataDict['newsSentiment_WeeklyAverage'] = json_resp.get('buzz').get('weeklyAverage')
        except: dataDict['newsSentiment_WeeklyAverage'] = None
        try: dataDict['newsSentiment_CompanyNewsScore'] = json_resp.get('companyNewsScore')
        except: dataDict['newsSentiment_CompanyNewsScore'] = None
        try: dataDict['newsSentiment_SectorAverageBullishPercent'] = json_resp.get('sectorAverageBullishPercent')
        except: dataDict['newsSentiment_SectorAverageBullishPercent'] = None
        try: dataDict['newsSentiment_SectorAverageNewsScore'] = json_resp.get('sectorAverageNewsScore')
        except: dataDict['newsSentiment_SectorAverageNewsScore'] = None
        try: dataDict['newsSentiment_BearishPercent'] = json_resp.get('sentiment').get('bearishPercent')
        except: dataDict['newsSentiment_BearishPercent'] = None
        try: dataDict['newsSentiment_BullishPercent'] = json_resp.get('sentiment').get('bullishPercent')
        except: dataDict['newsSentiment_BullishPercent'] = None

        yield scrapy.Request(
            url=f"https://finnhub.io/api/v1/stock/recommendation?symbol={dataDict['Symbol']}&from={self.SEVEN_DAYS_BACK}&to={self.TODAY}&token={self.API_TOKEN_FREE}",
            callback=self.recommendationTrends,
            meta={
                'dataDict': dataDict,
                'fileName': response.request.meta['fileName']
            }
        )

    def recommendationTrends(self, response):
        dataDict = response.request.meta['dataDict']
        json_resp = json.loads(response.body)

        #dataDict[f'Symbol'] = json_resp[0].get('symbol'))
        try: dataDict['recommendationTrends_Buy'] = json_resp[0].get('buy')
        except: dataDict['recommendationTrends_Buy'] = None
        try: dataDict['recommendationTrends_Hold'] = json_resp[0].get('hold')
        except: dataDict['recommendationTrends_Hold'] = None
        try: dataDict['recommendationTrends_Period'] = json_resp[0].get('period')
        except: dataDict['recommendationTrends_Period'] = None
        try: dataDict['recommendationTrends_Sell'] = json_resp[0].get('sell')
        except: dataDict['recommendationTrends_Sell'] = None
        try: dataDict['recommendationTrends_StrongBuy'] = json_resp[0].get('strongBuy')
        except: dataDict['recommendationTrends_StrongBuy'] = None
        try: dataDict['recommendationTrends_StrongSell'] = json_resp[0].get('strongSell')
        except: dataDict['recommendationTrends_StrongSell'] = None

        indx = [1,3,6]
        for idx,val in enumerate(indx,1):
            #dataDict[f'Symbol{idx}'] = json_resp[val].get('symbol'))
            try: dataDict[f'recommendationTrends_Buy{idx}'] = json_resp[val].get('buy')
            except: dataDict[f'recommendationTrends_Buy{idx}'] = None
            try: dataDict[f'recommendationTrends_Hold{idx}'] = json_resp[val].get('hold')
            except: dataDict[f'recommendationTrends_Hold{idx}'] = None
            try: dataDict[f'recommendationTrends_Period{idx}'] = json_resp[val].get('period')
            except: dataDict[f'recommendationTrends_Period{idx}'] = None
            try: dataDict[f'recommendationTrends_Sell{idx}'] = json_resp[val].get('sell')
            except: dataDict[f'recommendationTrends_Sell{idx}'] = None
            try: dataDict[f'recommendationTrends_StrongBuy{idx}'] = json_resp[val].get('strongBuy')
            except: dataDict[f'recommendationTrends_StrongBuy{idx}'] = None
            try: dataDict[f'recommendationTrends_StrongSell{idx}'] = json_resp[val].get('strongSell')
            except: dataDict[f'recommendationTrends_StrongSell{idx}'] = None

        yield scrapy.Request(
            url=f"https://finnhub.io/api/v1/stock/metric?symbol={dataDict['Symbol']}&metric=all&from={self.SEVEN_DAYS_BACK}&to={self.TODAY}&token={self.API_TOKEN_FREE}",
            callback=self.companyBasicFinancials,
            meta={
                'dataDict': dataDict,
                'fileName': response.request.meta['fileName']
            }
        )

    def companyBasicFinancials(self, response):
        dataDict = response.request.meta['dataDict']
        json_resp = json.loads(response.body)

        #dataDict['Symbol'] = json_resp.get('symbol'))
        try: dataDict['companyBasicFinancials_10DayAverageTradingVolume'] = json_resp.get('metric').get('10DayAverageTradingVolume')
        except: dataDict['companyBasicFinancials_10DayAverageTradingVolume'] = None
        try: dataDict['companyBasicFinancials_52WeekHigh'] = json_resp.get('metric').get('52WeekHigh')
        except: dataDict['companyBasicFinancials_52WeekHigh'] = None
        try: dataDict['companyBasicFinancials_52WeekLow'] = json_resp.get('metric').get('52WeekLow')
        except: dataDict['companyBasicFinancials_52WeekLow'] = None
        try: dataDict['companyBasicFinancials_52WeekLowDate'] = json_resp.get('metric').get('52WeekLowDate')
        except: dataDict['companyBasicFinancials_52WeekLowDate'] = None
        try: dataDict['companyBasicFinancials_52WeekPriceReturnDaily'] = json_resp.get('metric').get('52WeekPriceReturnDaily')
        except: dataDict['companyBasicFinancials_52WeekPriceReturnDaily'] = None

        #yield dataDict

        yield scrapy.Request(
            url=f'''https://finnhub.io/api/v1/scan/technical-indicator?symbol={dataDict['Symbol']}&resolution=D&token={self.API_TOKEN_FREE}''',
            callback=self.aggregateIndicator_day,
            meta={
                'dataDict': dataDict,
                'fileName': response.request.meta['fileName']
            }
        )

    def aggregateIndicator_day(self, response):
        dataDict = response.request.meta['dataDict']
        json_resp = json.loads(response.body)

        try: dataDict['TA_Daily_Buy'] = json_resp.get('technicalAnalysis').get('count').get('buy')
        except: dataDict['TA_Daily_Buy'] = None
        try: dataDict['TA_Daily_Neutral'] = json_resp.get('technicalAnalysis').get('count').get('neutral')
        except: dataDict['TA_Daily_Neutral'] = None
        try: dataDict['TA_Daily_Sell'] = json_resp.get('technicalAnalysis').get('count').get('sell')
        except: dataDict['TA_Daily_Sell'] = None
        try: dataDict['TA_Daily_Signal'] = json_resp.get('technicalAnalysis').get('signal')
        except: dataDict['TA_Daily_Signal'] = None
        try: dataDict['TA_Daily_ADX'] = json_resp.get('trend').get('adx')
        except: dataDict['TA_Daily_ADX'] = None
        try: dataDict['TA_Daily_trending'] = json_resp.get('trend').get('trending')
        except: dataDict['TA_Daily_trending'] = None

        yield scrapy.Request(
            url=f'''https://finnhub.io/api/v1/scan/technical-indicator?symbol={dataDict['Symbol']}&resolution=W&token={self.API_TOKEN_FREE}''',
            callback=self.aggregateIndicator_week,
            meta={
                'dataDict': dataDict,
                'fileName': response.request.meta['fileName']
            }
        )

    def aggregateIndicator_week(self, response):
        dataDict = response.request.meta['dataDict']
        json_resp = json.loads(response.body)

        try: dataDict['TA_Weekly_Buy'] = json_resp.get('technicalAnalysis').get('count').get('buy')
        except: dataDict['TA_Weekly_Buy'] = None
        try: dataDict['TA_Weekly_Neutral'] = json_resp.get('technicalAnalysis').get('count').get('neutral')
        except: dataDict['TA_Weekly_Neutral'] = None
        try: dataDict['TA_Weekly_Sell'] = json_resp.get('technicalAnalysis').get('count').get('sell')
        except: dataDict['TA_Weekly_Sell'] = None
        try: dataDict['TA_Weekly_Signal'] = json_resp.get('technicalAnalysis').get('signal')
        except: dataDict['TA_Weekly_Signal'] = None
        try: dataDict['TA_Weekly_ADX'] = json_resp.get('trend').get('adx')
        except: dataDict['TA_Weekly_ADX'] = None
        try: dataDict['TA_Weekly_trending'] = json_resp.get('trend').get('trending')
        except: dataDict['TA_Weekly_trending'] = None

        yield scrapy.Request(
            url=f'''https://finnhub.io/api/v1/scan/technical-indicator?symbol={dataDict['Symbol']}&resolution=M&token={self.API_TOKEN_FREE}''',
            callback=self.aggregateIndicator_month,
            meta={
                'dataDict': dataDict,
                'fileName': response.request.meta['fileName']
            }
        )

    def aggregateIndicator_month(self, response):
        fileName = response.request.meta['fileName']
        dataDict = response.request.meta['dataDict']
        json_resp = json.loads(response.body)

        try: dataDict['TA_Monthly_Buy'] = json_resp.get('technicalAnalysis').get('count').get('buy')
        except: dataDict['TA_Monthly_Buy'] = None
        try: dataDict['TA_Monthly_Neutral'] = json_resp.get('technicalAnalysis').get('count').get('neutral')
        except: dataDict['TA_Monthly_Neutral'] = None
        try: dataDict['TA_Monthly_Sell'] = json_resp.get('technicalAnalysis').get('count').get('sell')
        except: dataDict['TA_Monthly_Sell'] = None
        try: dataDict['TA_Monthly_Signal'] = json_resp.get('technicalAnalysis').get('signal')
        except: dataDict['TA_Monthly_Signal'] = None
        try: dataDict['TA_Monthly_ADX'] = json_resp.get('trend').get('adx')
        except: dataDict['TA_Monthly_ADX'] = None
        try: dataDict['TA_Monthly_trending'] = json_resp.get('trend').get('trending')
        except: dataDict['TA_Monthly_trending'] = None

        yield scrapy.Request(
            url=f"https://finnhub.io/api/v1/stock/price-target?symbol={dataDict['Symbol']}&token={self.API_TOKEN_PAID}",                
            callback=self.revenueEstimates,
            meta={
                'dataDict': dataDict,
                'fileName': fileName
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
            url=f"https://finnhub.io/api/v1/stock/revenue-estimate?symbol={dataDict['Symbol']}&freq=quarterly&token={self.API_TOKEN_PAID}",                
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
            url=f"https://finnhub.io/api/v1/stock/eps-estimate?symbol={dataDict['Symbol']}&freq=quarterly&token={self.API_TOKEN_PAID}",                
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
            url=f"https://finnhub.io/api/v1/stock/earnings?symbol={dataDict['Symbol']}&token={self.API_TOKEN_PAID}",                
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
        self.writeCSV(dataDict, self.field_names, f'data/{fileName.replace("symbols","data")}')
