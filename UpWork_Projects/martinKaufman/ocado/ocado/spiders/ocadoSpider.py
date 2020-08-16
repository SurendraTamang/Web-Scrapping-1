import scrapy
import time
from scrapy import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class OcadospiderSpider(scrapy.Spider):
    name = 'ocadoSpider'

    categoryURLs = [
        #'https://www.ocado.com/webshop/getCategories.do?tags=%7C20002&Abutton=1',
        #'https://www.ocado.com/webshop/getCategories.do?tags=%7C20424&Abutton=1',
        #'https://www.ocado.com/webshop/getCategories.do?tags=%7C25189&Abutton=1',
        #'https://www.ocado.com/webshop/getCategories.do?tags=%7C20911&Abutton=1',
        #'https://www.ocado.com/webshop/getCategories.do?tags=%7C20977&Abutton=1',
        'https://www.ocado.com/webshop/getCategories.do?tags=%7C30489&Abutton=1'
    ]

    def genURLs(self, value):
        li = value.split(" ")
        return f'''https://www.myfitnesspal.com/food/search?page=1&search={"%20".join(str(i) for i in li)}'''

    def qty_fix(self, value):
        try:
            return f"{value[1]}{value[3]}"
        except:
            return None

    def start_requests(self):
        yield SeleniumRequest(
            url="https://groceries.morrisons.com",
            wait_time=5,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        driver.maximize_window()
        for categoryURL in self.categoryURLs:
            driver.get(categoryURL)
            
            html1 = driver.page_source
            response1 = Selector(text=html1)

            catURLs = response1.xpath("//div[contains(@class, 'level-0')]/ul/li")

            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])

            for catURL in catURLs:
                url = f'''https://www.ocado.com{catURL.xpath(".//a/@href").get()}'''
                driver.get(url)
                driver.execute_script("window.scrollTo(0, 1500);")
                time.sleep(3)

                html2 = driver.page_source
                response2 = Selector(text=html2)

                subCatURLs = response2.xpath("//div[contains(@class, 'level-0')]/ul/li")
                if subCatURLs:
                    driver.execute_script("window.open('');")
                    driver.switch_to.window(driver.window_handles[2])
                    for subCatURL in subCatURLs:
                        url = f'''https://www.ocado.com{subCatURL.xpath(".//a/@href").get()}'''
                        driver.get(url)
                        driver.execute_script("window.scrollTo(0, 2500);")
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(3)

                        html3 = driver.page_source
                        response3 = Selector(text=html3)
                        products = response3.xpath("//ul[contains(@class, 'fops-shelf')]/li")
                        
                        for product in products:
                            url = f'''https://www.ocado.com{product.xpath(".//div[@role='presentation']/a/@href").get()}'''
                            if url != "https://www.ocado.comNone":
                                yield {
                                    'url': url
                                }
                                # yield scrapy.Request(
                                #     url=url,
                                #     callback=self.prodDetails,
                                #     dont_filter=True
                                # )
                    driver.close()  
                    driver.switch_to.window(driver.window_handles[1])
                else:
                    products = response2.xpath("//ul[contains(@class, 'fops-shelf')]/li")
                    
                    for product in products:
                        url = f'''https://www.ocado.com{product.xpath(".//div[@role='presentation']/a/@href").get()}'''
                        if url != "https://www.ocado.comNone":
                            yield {
                                'url': url
                            }
                            # yield scrapy.Request(
                            #     url=url,
                            #     callback=self.prodDetails,
                            #     dont_filter=True
                            # )
                            
            driver.close()  
            driver.switch_to.window(driver.window_handles[0])

    def prodDetails(self, response):
        productName = response.xpath("normalize-space(//header[@class='bop-title']/h2/text())").get()
        quantity = response.xpath("normalize-space(//header[@class='bop-title']/h2/span/text())").get()
        price = response.xpath("normalize-space(//h2[contains(@class, 'bop-price__current ')]/text())").get()
        img_url = f'''https://www.ocado.com{response.xpath("//img[@role='presentation']/@src").get()}'''
        url = response.url
        
        if quantity == None:
            quantity = "1 Piece"
        cal1 = response.xpath("//table/tbody/tr[3]/td[1]/text()").get()
        if cal1 != None:
            if "energy" in cal1.lower():            
                cal2 = response.xpath("//table/tbody/tr[3]/td[2]/text()").get()
                cal3 = response.xpath("//table/tbody/tr[3]/td[3]/text()").get()
            else:
                cal1 = response.xpath("//table/tbody/tr[2]/td[1]/text()").get()
                cal2 = response.xpath("//table/tbody/tr[2]/td[2]/text()").get()
                cal3 = response.xpath("//table/tbody/tr[2]/td[3]/text()").get()
        else:
            cal1 = response.xpath("//table/tbody/tr[2]/td[1]/text()").get()
            cal2 = response.xpath("//table/tbody/tr[2]/td[2]/text()").get()
            cal3 = response.xpath("//table/tbody/tr[2]/td[3]/text()").get()

        if cal1 != None or cal2 != None:
            yield {
                'productName': productName,
                'quantity': quantity,
                'price': price,
                'img_url': img_url,
                'url': url,
                'cal1': cal1,
                'cal2': cal2,
                'cal3': cal3,
                'calPerQty': None,
                'calories': None
            }
        else:
            yield scrapy.Request(
                url=self.genURLs(productName),
                callback=self.getCalDetails,
                dont_filter=True,
                meta={
                    'productName': productName,
                    'quantity': quantity,
                    'price': price,
                    'img_url': img_url,
                    'url': url,
                    'cal1': cal1,
                    'cal2': cal2,
                    'cal3': cal3
                }
            )

    def getCalDetails(self, response):
        calPerQty = self.qty_fix(response.xpath("(//div[@class='jss9'])[1]/text()").getall())
        # calPerQty = response.xpath("(//div[@class='jss9'])[1]/text()").getall()
        calories = response.xpath("//div[@class='jss14']/text()").get()
        if calPerQty == None:
            calPerQty = response.xpath("(//div[@class='jss9'])[1]/text()").getall()
            calPerQty = "".join(str(i) for i in calPerQty)

        yield {
            'productName': response.request.meta['productName'],
            'quantity': response.request.meta['quantity'],
            'price': response.request.meta['price'],
            'img_url': response.request.meta['img_url'],
            'url': response.request.meta['url'],
            'cal1': response.request.meta['cal1'],
            'cal2': response.request.meta['cal2'],
            'cal3': response.request.meta['cal3'],
            'calPerQty': calPerQty,
            'calories': calories.replace("Calories: ", "")
        }
