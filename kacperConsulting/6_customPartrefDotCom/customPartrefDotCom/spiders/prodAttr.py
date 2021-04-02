import scrapy
from scrapy import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd


class ProdattrSpider(scrapy.Spider):
    name = 'prodAttr'

    df = pd.read_excel("D:/Web-Scrapping/UpWork_Projects/kacper/oldData/prodAttrMS.xlsx", sheet_name="Sheet2")
    
    def start_requests(self):
        yield SeleniumRequest(
            url='https://www.google.com',
            wait_time=10,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        driver.maximize_window()
        cntr_xyz = 0
        for _,val in self.df.iterrows():
            if cntr_xyz == 0 or cntr_xyz%5 == 0:
                driver.get('http://custom.partref.com/AGR#')
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@id='txtPartNO']")))
                #driver.execute_script("document.body.style.zoom='70%'")
                driver.execute_script("document.body.style.transform = 'scale(0.6)'")
                driver.execute_script(f"window.scrollTo(0, 150);")
                time.sleep(3)
            cntr_xyz += 1          
            
            input_field = driver.find_element_by_xpath("//input[@id='txtPartNO']")
            input_field.clear()
            input_field.send_keys(val['Interchange no'])
            driver.find_element_by_xpath("//input[@id='search']").click()
            try:
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//tbody/tr[@class='odd' or @class='even']")))
            except:
                pass

            try:
                alert_obj = driver.switch_to.alert
                avlty = alert_obj.text
                if avlty == "Searched Result Not Found":
                    alert_obj.accept()
            except:
                pass
            try:
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Name']")))
            except:
                pass
            driver.execute_script(f"window.scrollTo(0, 150);")
            name_field = driver.find_element_by_xpath("//input[@placeholder='Name']")
            name_field.clear()
            name_field.send_keys("Armature")
            time.sleep(3)

            # #   GETTING THE PAGE HEIGHT & SCROLLING GRADUALLY THROUGH THE PAGE TO LAOD ALL THE ELEMENTS #
            # height = driver.execute_script("return document.body.scrollHeight")
            # for i in range(1, (height//200)+1):
            #     driver.execute_script(f"window.scrollTo(0, {i*200});")
            #     time.sleep(0.1)

            cntr = 1
            while True:
                cntr += 1
                driver.execute_script(f"window.scrollTo(0, 600);")
                driver.execute_script(f"window.scrollTo(0, -600);")
                html = driver.page_source
                resp_obj = Selector(text=html)
                noOfPgs = resp_obj.xpath("(//div/span)[last()]/a[contains(@class, 'paginate_button')][last()]/text()").get()

                parts = resp_obj.xpath("//tbody/tr[@class='odd' or @class='even']")
                for cntr,part in enumerate(parts):
                    if part.xpath(".//td[contains(@id,'appbomlist')]/a"):
                        driver.find_element_by_xpath(f"(//tbody/tr[@class='odd' or @class='even']//td[contains(@id,'appbomlist')])[{cntr+1}]").click()
                        try:
                            driver.find_element_by_xpath(f"(//tbody/tr[@class='odd' or @class='even']//td[contains(@id,'appbomlist')])[{cntr+1}]").click()
                        except:
                            pass
                        # driver.find_element_by_xpath(f"(//tbody/tr[@class='odd' or @class='even']//td)[{cntr+1}]").click()
                        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//h2[@id='hdrPart']")))
                        htmlInnr = driver.page_source
                        resp_obj_innr = Selector(text=htmlInnr)
                        partImgUrl = resp_obj_innr.xpath("//ul[@id='UlUnitImageSlider']/li/img/@src").getall()
                        yield {
                            'Interchange (Search Number)': val['Interchange no'],
                            'Name': "Armature G Roy",
                            'Part Number to label images': val['image labels'],
                            'Manufacture': resp_obj_innr.xpath("normalize-space(//td[contains(text(), 'Manufacture')]/following-sibling::td/text())").get(),
                            'Amperage Rating': resp_obj_innr.xpath("normalize-space(//td[contains(text(), 'Amperage Rating')]/following-sibling::td/text())").get(),
                            'Decoupled Or Clutch Pulley': resp_obj_innr.xpath("normalize-space(//td[contains(text(), 'Decoupled Or Clutch Pulley')]/following-sibling::td/text())").get(),
                            'Fan Type': resp_obj_innr.xpath("normalize-space(//td[contains(text(), 'Fan Type')]/following-sibling::td/text())").get(),
                            'Ground Type': resp_obj_innr.xpath("normalize-space(//td[contains(text(), 'Ground')]/following-sibling::td/text())").get(),
                            'Plug Clock Rear View Main Mounting Ear at 6 O Clock': resp_obj_innr.xpath("normalize-space(//td[contains(text(), 'Plug Clock Rear View')]/following-sibling::td/text())").get(),
                            'Plug Type': resp_obj_innr.xpath("normalize-space(//td[contains(text(), 'Plug Type')]/following-sibling::td/text())").get(),
                            'Pulley Belt Type': resp_obj_innr.xpath("normalize-space(//td[contains(text(), 'Pulley Belt Type')]/following-sibling::td/text())").get(),
                            'Pulley Groove Quantity': resp_obj_innr.xpath("normalize-space(//td[contains(text(), 'Pulley Groove Quantity')]/following-sibling::td/text())").get(),
                            'Pulley Outside Diameter': resp_obj_innr.xpath("normalize-space(//td[contains(text(), 'Pulley Outside Diameter')]/following-sibling::td/text())").get(),
                            'Regulator Type': resp_obj_innr.xpath("normalize-space(//td[contains(text(), 'Regulator Type')]/following-sibling::td/text())").get(),
                            'Rotation Direction': resp_obj_innr.xpath("normalize-space(//td[contains(text(), 'Rotation')]/following-sibling::td/text())").get(),
                            'Voltage': resp_obj_innr.xpath("normalize-space(//td[contains(text(), 'Voltage')]/following-sibling::td/text())").get(),
                            'Circuit Type': resp_obj_innr.xpath("normalize-space(//td[contains(text(), 'Circuit Type')]/following-sibling::td/text())").get(),
                            'Design': resp_obj_innr.xpath("normalize-space(//td[contains(text(), 'Design')]/following-sibling::td/text())").get(),
                            'Mounting Bolt Hole Quantity': resp_obj_innr.xpath("normalize-space(//td[contains(text(), 'Mounting Bolt Hole Quantity')]/following-sibling::td/text())").get(),
                            'Mounting Type': resp_obj_innr.xpath("normalize-space(//td[contains(text(), 'Mounting Type')]/following-sibling::td/text())").get(),
                            'Power Rating': resp_obj_innr.xpath("normalize-space(//td[contains(text(), 'Power Rating')]/following-sibling::td/text())").get(),
                            'Family': resp_obj_innr.xpath("normalize-space(//td[contains(text(), 'Family')]/following-sibling::td/text())").get(),
                            'Clock Position': resp_obj_innr.xpath("normalize-space(//td[contains(text(), 'Clock Position')]/following-sibling::td/text())").get(),
                            'Starter Drive Housing Position': resp_obj_innr.xpath("normalize-space(//td[contains(text(), 'Starter Drive Housing Position')]/following-sibling::td/text())").get(),
                            'Tooth Quantity': resp_obj_innr.xpath("normalize-space(//td[contains(text(), 'Tooth Quantity')]/following-sibling::td/text())").get(),
                            'Stator Type': resp_obj_innr.xpath("normalize-space(//td[contains(text(), 'Stator Type')]/following-sibling::td/text())").get(),
                            'Part Image Url': ",".join(piu for piu in partImgUrl if "na.jpg" not in piu),
                            'Plug Image Url': resp_obj_innr.xpath("//td[@id='plugimages']/img/@src").get(),
                        }
                        driver.find_element_by_xpath("//a[contains(text(), 'List Search')]/parent::li").click()
                        time.sleep(1)
                        driver.execute_script(f"window.scrollTo(0, 600);")
                        #input()
                # if cntr <= int(noOfPgs):
                try:
                    driver.execute_script(f"window.scrollTo(0, -1000);")
                    time.sleep(1)
                    WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, "(//a[text()='Next'])[2]"))).click()
                    time.sleep(2)
                except:
                    break
                # else:
                #     break