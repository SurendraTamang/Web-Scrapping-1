import scrapy
import json
import os
import csv
from datetime import datetime, date, timedelta


class EcalendarSpider(scrapy.Spider):
    name = 'eCalendar'
    
    #--Column Names--#
    FIELD_NAME = ['Symbol', 'Time', 'Company Name', 'EPS', 'Surprise Percent', 'Market Cap', 'Fisical Quarter Ending', 'Consensus EPS Forecast', 'No of Ests', 'Last Year Report Date', 'Last year EPS']
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66',
        'accept': "application/json, text/plain, */*",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "en-US,en;q=0.9"
    }
    
    #--Generate the week Number--#
    # WEEK_NUM = None
    # todayWeekNum = datetime.today().weekday()
    # if todayWeekNum == 5 or todayWeekNum == 6:
    #     WEEK_NUM = date.today().isocalendar()[1] + 1 
    # else:
    #     WEEK_NUM = date.today().isocalendar()[1]

    #--Creating a folder for the current week data--#
    # if not os.path.exists(f"data/week_{WEEK_NUM}"):
    #     os.mkdir(f"data/week_{WEEK_NUM}")

    #Monday is 0 and Sunday is 6
    def getCurrWeekDates(self):
        todayWeekNum = datetime.today().weekday()
        dateList = []
        #--MONDAY--#
        if todayWeekNum == 0:
            dateList = [(date.today() + timedelta(days=int(f'{i}'))).strftime("%Y-%m-%d") for i in range(0,5)]
        #--TUESDAY--#
        elif todayWeekNum == 1:
            dateList = [(date.today() + timedelta(days=int(f'{i}'))).strftime("%Y-%m-%d") for i in range(0,4)]
            dateList.insert(0, (date.today() - timedelta(days=1)).strftime("%Y-%m-%d"))
        #--WEDNESDAY--#
        elif todayWeekNum == 2:
            dateList = [(date.today() + timedelta(days=int(f'{i}'))).strftime("%Y-%m-%d") for i in range(0,3)]
            dateList.insert(0, (date.today() - timedelta(days=2)).strftime("%Y-%m-%d"))
            dateList.insert(1, (date.today() - timedelta(days=1)).strftime("%Y-%m-%d"))
        #--THURSDAY--#
        elif todayWeekNum == 3:
            dateList = [(date.today() - timedelta(days=int(f'{i}'))).strftime("%Y-%m-%d") for i in range(0,4)]
            dateList.insert(0, (date.today() + timedelta(days=1)).strftime("%Y-%m-%d"))
            dateList.reverse()
        #--FRIDAY--#
        elif todayWeekNum == 4:
            dateList = [(date.today() - timedelta(days=int(f'{i}'))).strftime("%Y-%m-%d") for i in range(0,5)]
            dateList.reverse()
        #--SATURDAY--#
        elif todayWeekNum == 5:
            dateList = [(date.today() + timedelta(days=int(f'{i}'))).strftime("%Y-%m-%d") for i in range(2,7)]
        #--SUNDAY--#
        elif todayWeekNum == 6:
            dateList = [(date.today() + timedelta(days=int(f'{i}'))).strftime("%Y-%m-%d") for i in range(1,6)]

        return dateList
    
    def writeCSV(self, data, fieldName, FILE_NAME):
        fileExists = os.path.isfile(FILE_NAME)
        with open(FILE_NAME, 'a', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldName, lineterminator='\n')
            if not fileExists:
                writer.writeheader()
            writer.writerow(data)

    def removeNA(self, val):
        if val == "NA":
            return None
        else:
             return val

    def start_requests(self):
        for dt in self.getCurrWeekDates():
            yield scrapy.Request(
                url=f"https://api.nasdaq.com/api/calendar/earnings?date={dt}",
                # method="GET",
                headers=self.headers,
                callback=self.parse,
                meta={
                    'date': dt
                }
            )

    def parse(self, response):
        dt = response.request.meta['date']
        jsonResp = json.loads(response.body)
        symbols = jsonResp.get('data').get('rows')
        for symbol in symbols:
            dataDict = {
                self.FIELD_NAME[0]: symbol.get('symbol'),
                self.FIELD_NAME[1]: symbol.get('time'),
                self.FIELD_NAME[2]: symbol.get('name'),
                self.FIELD_NAME[3]: symbol.get('eps'),
                self.FIELD_NAME[4]: symbol.get('surprise'),
                self.FIELD_NAME[5]: symbol.get('marketCap'),
                self.FIELD_NAME[6]: symbol.get('fiscalQuarterEnding'),
                self.FIELD_NAME[7]: symbol.get('epsForecast'),
                self.FIELD_NAME[8]: symbol.get('noOfEsts'),
                self.FIELD_NAME[9]: self.removeNA(symbol.get('lastYearRptDt')),
                self.FIELD_NAME[10]: self.removeNA(symbol.get('lastYearEPS')),
            }
            
            print(dataDict)
            #self.writeCSV(dataDict, self.FIELD_NAME, f'data/week_{self.WEEK_NUM}/symbols_{dt}.csv')
            self.writeCSV(dataDict, self.FIELD_NAME, f'data/symbols_{dt}.csv')
