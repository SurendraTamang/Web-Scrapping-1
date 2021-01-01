import scrapy
from scrapy import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import random
import string
import os
import csv
import pandas as pd


class FotoSpider(scrapy.Spider):
    name = 'foto'

    inputURLs = pd.read_excel("inputURLS.xlsx")
    dfinputURLs = inputURLs['URLS'].to_list()

    #   READING THE CSV FILE    #
    FILEPATH = "fotocasaData.csv"
    df = pd.read_csv(FILEPATH)
    dfList = df['Url'].to_list()

    #  TAKING USER INPUTS  #
    print("============================================================================================")
    print("\n\nWELCOME TO fotocasa SCRAPER\n\n")
    print("============================================================================================")
    province = input("ENTER THE PROVINCE NAME : ")
    area = list(map(str, input("ENTER THE AREA ( separate multiple values with , ) : ").rstrip().split(',')))
    buyRent = input("\nENTER THE TYPE (buy / rent / both) : ")  
    room = input("NO. OF ROOMS (all, 1, 2, 3, 4) : ")
    bath = input("NO. OF BATHROOMS (all, 1, 2, 3) : ")
    print("============================================================================================")
    print("\n\nTHANKS FOR THE INPUTS. STARTING THE SCRAPER\n\n")
    print("============================================================================================")

    #   WRITING THE DATA INTO CSV FILE  #
    def writeCSV(self, dict_data, fieldName):
        with open(self.FILEPATH, 'a', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldName, lineterminator='\n')
            # if not self.FILE_EXISTS:
            #     writer.writeheader()
            for data in dict_data:
                writer.writerow(data)

    #   FUNCTION TO GENEARTE URLS CITY WISE (BUY/RENT)  #
    def genBuyRentUrl(self, usrInpt, urlList):
        urlLi = []
        for url in urlList:
            if usrInpt == "buy":
                urlLi.append(url)
            elif usrInpt == "rent":
                urlLi.append(url.replace("comprar", "alquiler"))
            else :
                urlLi.append(url)
                urlLi.append(url.replace("comprar", "alquiler"))
        return urlLi

    #   FUNCTION TO GENERATE RANDOM EMAILS  #
    def gen_random_email(self):
        return f'''{"".join(random.choice(string.ascii_lowercase) for _ in range(random.randint(5,10)))}@gmail.com'''
    
    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.fotocasa.es/es",
            wait_time=5,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[0])
        driver.maximize_window()

        #   ACCEPTING THE COOKIES   #
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), 'Aceptar y cerrar')]/parent::button"))).click()
        except:
            pass

        #   GETTING CITY WISE URLs    #
        # driver.find_element_by_xpath("//span[text()='Comprar']/parent::li").click()
        # time.sleep(1)
        # html1 = driver.page_source
        # respObj1 = Selector(text=html1)
        # cityUrls = respObj1.xpath("(//ul[contains(@class,'ListLink')])[1]/li/a/@href").getall()
        urlList = self.genBuyRentUrl(self.buyRent, self.dfinputURLs)

        #   LOOPING OVER THE CITY WISE URLS #
        inpAraLen = len(self.area)
        cntr = 0
        if self.buyRent == "both":
            inpAraLen *= 2
        for url in urlList:
            if cntr < inpAraLen and self.area[cntr] in url:
                areaAddr = self.area[cntr]
                cntr += 1
                driver.get(url)
                time.sleep(1)
                WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//article[contains(@class,'Searchresult')]")))            

                #   APPLYING THE FILTERS    #
                if self.room:
                    if self.room != "all":
                        WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.XPATH, "//span[text()='Habitaciones']/parent::div"))).click()
                        WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.XPATH, f"//div[text()='Habitaciones']/following-sibling::div/button[{int(self.room)+1}]"))).click()
                        WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), 'anuncios')]/parent::button"))).click()
                        time.sleep(1)
                        try:
                            WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.XPATH, "//span[text()='No, gracias']/parent::button"))).click()
                        except:
                            pass
                            
                if self.bath:
                    if self.bath != "all":
                        WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.XPATH, "//span[text()='Baños']/parent::div"))).click()
                        WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.XPATH, f"//div[text()='Baños']/following-sibling::div/button[{int(self.bath)+1}]"))).click()
                        WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), 'anuncios')]/parent::button"))).click()
                        time.sleep(1)
                        try:
                            WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.XPATH, "//span[text()='No, gracias']/parent::button"))).click()
                        except:
                            pass

                #   LOOPING OVER THE ADs LISTING    #
                while True:
                    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//article[contains(@class,'Searchresult')]")))
                    
                    #   GETTING THE PAGE HEIGHT & SCROLLING GRADUALLY THROUGH THE PAGE TO LAOD ALL THE ELEMENTS #
                    height = driver.execute_script("return document.body.scrollHeight")
                    for i in range(1, (height//200)+1):
                        driver.execute_script(f"window.scrollTo(0, {i*200});")
                        time.sleep(0.1)
                    

                    #   EXTRACTING THE WEBSITE'S DOM    #
                    html = driver.page_source
                    respObj = Selector(text=html)

                    articles = respObj.xpath("//article[contains(@class,'Searchresult')]")
                    driver.switch_to.window(driver.window_handles[1])
                    for article in articles:
                        if article.xpath(".//a[contains(@href, 'tel:')]") or article.xpath(".//div[contains(@class, 'promotionLogo')]") or f'''https://www.fotocasa.es{article.xpath(".//a/@href").get()}''' in self.dfList:
                            pass
                        else:
                            try:
                                driver.get(f'''https://www.fotocasa.es{article.xpath(".//a/@href").get()}''')

                                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//a[contains(text(), 'Ver teléfono')]/parent::div")))
                                html_pvt_own_check = driver.page_source
                                respObj_pvt_own_check = Selector(text=html_pvt_own_check)

                                #   CHECK TO IDDENTIFY A PRIVER OWNER OR NOT    #
                                if respObj_pvt_own_check.xpath("normalize-space((//span[contains(@class, 'ContactDetail-particularName')])[1]/text())").get():
                                    
                                    #   FILLING THE FORM TO VIEW THE CONTACT NUMBER #
                                    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//a[contains(text(), 'Ver teléfono')]/parent::div"))).click()                                
                                    email_field = driver.find_element_by_xpath("//div[text()='Ver teléfono']/parent::div/parent::div//input[contains(@placeholder, 'e-mail')]")
                                    email_field.clear()
                                    email_field.send_keys(self.gen_random_email())
                                    driver.find_element_by_xpath("(//div[text()='Ver teléfono']/parent::div/parent::div//label)[last()]/parent::div").click()
                                    time.sleep(1)
                                    driver.find_element_by_xpath("//div[text()='Ver teléfono']/parent::div/parent::div//span[text()='Contactar']/parent::span/parent::button").click()
                                    time.sleep(2)
                                    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "(//div[contains(@class, 'ContactDetail-phone')])[1]")))

                                    #   GETTING THE PAGE HEIGHT & SCROLLING GRADUALLY THROUGH THE PAGE TO LAOD ALL THE ELEMENTS #
                                    heightInr = driver.execute_script("return document.body.scrollHeight")
                                    for i in range(1, heightInr//500):          
                                        driver.execute_script(f"window.scrollTo(0, {i*500});")

                                    #   EXTRACTING DATA POINTS THE WEBSITE'S DOM    #
                                    html_innr = driver.page_source
                                    respObj_innr = Selector(text=html_innr)

                                    # ftrs = respObj_innr.xpath("//ul[contains(@class, 'DetailExtras')]/li/text()").getall()
                                    propTitle = respObj_innr.xpath("normalize-space(//h1[contains(@class, 'propertyTitle')]/text())").get()
                                    addr = f'''{propTitle.split(" en ")[-1]}, {areaAddr}, {self.province}'''
                                    images = respObj_innr.xpath("//section/figure/img/@src").get()
                                    rentSale = None
                                    if "comprar" in url:
                                        rentSale = "Sale"
                                    elif "alquiler" in url:
                                        rentSale = "Rent"
                                    dataList=[]
                                    dataList.append(
                                        {
                                            'Property Title': propTitle,
                                            'Bed': respObj_innr.xpath("normalize-space(//span[contains(text(),'hab')]/span/text())").get(),
                                            'Bath': respObj_innr.xpath("normalize-space(//span[contains(text(),'baño')]/span/text())").get(),
                                            'Area in meter sq': respObj_innr.xpath("normalize-space(//span[contains(text(),'m²')]/span/text())").get(),
                                            'Price': respObj_innr.xpath("normalize-space(//span[contains(@class,'price')]/text())").get(),
                                            'Owner Name': respObj_innr.xpath("normalize-space((//span[contains(@class, 'ContactDetail-particularName')])[1]/text())").get(),
                                            'Phone': f'''{respObj_innr.xpath("normalize-space((//div[contains(@class, 'ContactDetail-phone')])[1]/text()[last()])").get()}''',
                                            'Reference No': f'''{respObj_innr.xpath("normalize-space(//label[text()='Referencia fotocasa']/following-sibling::span/text())").get()}''',
                                            # 'Features': " , ".join(ftr.strip() for ftr in ftrs),
                                            'Type': respObj_innr.xpath("normalize-space(//p[text()='Tipo de inmueble']/following-sibling::p/text())").get(),
                                            'Rent/Sale': rentSale,
                                            'Address': addr,
                                            'Images': images,
                                            'Url': driver.current_url
                                        }
                                    )
                                    self.writeCSV(dataList, ["Property Title", "Bed", "Bath", "Area in meter sq", "Price", "Owner Name", "Phone", "Reference No", "Type", "Rent/Sale", "Address", "Images", "Url"])
                            except:
                                pass
                    driver.switch_to.window(driver.window_handles[0])

                    #   HANDLING THE PAGINATION   #
                    nextPage = respObj.xpath("//a[text()='>']/@href").get()
                    if nextPage:
                        driver.get(f'''https://www.fotocasa.es{nextPage}''')
                    else:
                        break

#   CODE SNIPPET FOR EXTRACTING PROVINCE & DISTRICT URLS    #
# #   ACCEPTING THE COOKIES   #
# try:
#     WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), 'Aceptar y cerrar')]/parent::button"))).click()
# except:
#     pass

# #   GETTING CITY WISE URLs    #
# driver.find_element_by_xpath("//span[text()='Comprar']/parent::li").click()
# time.sleep(1)
# html1 = driver.page_source
# respObj1 = Selector(text=html1)
# cityUrls = respObj1.xpath("(//ul[contains(@class,'ListLink')])[1]/li/a/@href").getall()
# for url in cityUrls:
#     driver.get(f'''https://www.fotocasa.es{url}''')
#     WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//article[contains(@class,'Searchresult')]")))

#     #   GETTING THE PAGE HEIGHT & SCROLLING GRADUALLY THROUGH THE PAGE TO LAOD ALL THE ELEMENTS #
#     height = driver.execute_script("return document.body.scrollHeight")
#     for i in range(1, (height//500)+1):
#         driver.execute_script(f"window.scrollTo(0, {i*500});")
#     time.sleep(2)

#     #   EXTRACTING THE WEBSITE'S DOM    #
#     html = driver.page_source
#     respObj = Selector(text=html)
#     dUrls = respObj.xpath("//h2[contains(text(), 'en la provincia')]/parent::section//ul/li/a/@href").getall()
#     for dUrl in dUrls:                
#         yield{
#             'Province Url': url,
#             'District Url': f'''https://www.fotocasa.es{dUrl}''',
#         }