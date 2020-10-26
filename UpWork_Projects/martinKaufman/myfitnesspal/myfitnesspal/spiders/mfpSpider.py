import scrapy
# import time
# from scrapy import Selector
# from scrapy_selenium import SeleniumRequest
import pandas as pd
# from selenium.webdriver.common.keys import Keys


class MfpspiderSpider(scrapy.Spider):
    name = 'mfpSpider'
    
    df = pd.read_excel("D:/Web-Scrapping/UpWork_Projects/martinKaufman/myfitnesspal/urls.xlsx")

    def genURLs(self, value):
        newValue = value.replace("&", "%26")
        newValue1 = newValue.replace("%","%25")
        newValue2 = newValue1.replace("Sainsbury's ","")
        li = newValue2.split(" ")
        # li = newValue1.split(" ")
        #if "ASDA" in newValue:
        return f'''https://www.myfitnesspal.com/food/search?page=1&search={"%20".join(str(i) for i in li)}'''
        # else:
        #     return f'''https://www.myfitnesspal.com/food/search?page=1&search={"%20".join(str(i) for i in li)}'''

    def qty_fix(self, value):
        try:
            # li = value[0].split(",")
            # word = "".join(i for i in li[-1:])
            # return word.strip()
            return f"{value[1]}{value[3]}"
        except:
            return None

    def start_requests(self):
        for _, value in self.df.iterrows():
            yield scrapy.Request(
                url=self.genURLs(value['productName']),
                callback=self.parse,
                dont_filter=True,
                meta={
                    'url': value['url'],
                    'productName': value['productName']
                }
            )
        # yield SeleniumRequest(
        #     url="https://www.myfitnesspal.com/food/search",
        #     wait_time=5,
        #     callback=self.parse
        # )

    def parse(self, response):
        calPerQty = self.qty_fix(response.xpath("(//div[@class='jss11'])[1]/text()").getall())
        # calPerQty = response.xpath("(//div[@class='jss9'])[1]/text()").getall()
        calories = response.xpath("//div[@class='jss16']/text()").get()
        if calPerQty == None:
            calPerQty = response.xpath("(//div[@class='jss11'])[1]/text()").getall()
            calPerQty = "".join(str(i) for i in calPerQty)
        try:
            caloriesNew = calories.replace("Calories: ", "")
        except:
            caloriesNew = calories

        yield {
            'productName': response.request.meta['productName'],
            'url': response.request.meta['url'],
            'Serving Size of Food Item': calPerQty,
            'Number of Calories Per Serving': caloriesNew
        }

        # driver = response.meta['driver']
        # driver.maximize_window()
        # for _, value in self.df.iterrows():
        #     productName = value['Name']
        #     url = value['product url']
        #     input_box = driver.find_element_by_xpath("//input[@type='search']")
        #     input_box.send_keys(f"{productName}, lidl")
        #     input_box.send_keys(Keys.ENTER)
        #     time.sleep(3)

        #     html = driver.page_source
        #     resp_obj = Selector(text=html)

        #     calPerQty = self.qty_fix(resp_obj.xpath("(//div[@class='jss49'])[1]/text()").getall())
        #     calories = resp_obj.xpath("//div[@class='jss54']/text()").get()

        #     yield {
        #         'productName': productName,
        #         'url': url,
        #         'calPerQty': calPerQty,
        #         'calories': calories.replace("Calories: ", "")
        #     }

        #     driver.find_element_by_xpath("//input[@type='search']").clear()
