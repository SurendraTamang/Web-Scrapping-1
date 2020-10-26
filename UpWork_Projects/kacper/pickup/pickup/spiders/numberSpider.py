import scrapy
from scrapy import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import pandas as pd
import time


class NumberspiderSpider(scrapy.Spider):
    name = 'numberSpider'

    df = pd.read_excel("D:/Web-Scrapping/UpWork_Projects/kacper/pickup/MasterSheet.xlsx", sheet_name='querySheet2')
    # df = pd.read_excel("D:/Web-Scrapping/UpWork_Projects/kacper/pickup/MasterSheet.xlsx", sheet_name='test')

    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.google.com/search?rlz=1C1RLNS_enIN908IN908&sxsrf=ALeKk03ypUHfLG2MqzBPAJ7AAi9KJEON0A%3A1601123225599&ei=mTNvX6OOJIK55gL9uqV4&q=YUNGASIGN+10+rue+4+alliances+26200+MONTELIMAR+france&oq=YUNGASIGN+10+rue+4+alliances+26200+MONTELIMAR+france&gs_lcp=CgZwc3ktYWIQAzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzoECCMQJ1C-eljLfGD3f2gBcAB4AIABxASIAcQEkgEDNS0xmAEAoAEBoAECqgEHZ3dzLXdperABCsABAQ&sclient=psy-ab&ved=0ahUKEwjjvuno6IbsAhWCnFkKHX1dCQ8Q4dUDCA0&uact=5",
            wait_time=5,
            callback=self.parse
        )

    def parse(self, response):
        i = 1
        driver = response.meta['driver']
        driver.maximize_window()
        driver.execute_script("window.open('');")
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(2)
        for _,value in self.df.iterrows():
            driver.find_element_by_xpath("//input[@aria-label='Search']").clear()
            searchInput = driver.find_element_by_xpath("//input[@aria-label='Search']")
            searchInput.send_keys(value['Query'])
            searchInput.send_keys(Keys.ENTER)
            time.sleep(3)
            html = driver.page_source
            respObj = Selector(text=html)
            phone = respObj.xpath("normalize-space(//span[contains(@aria-label, 'Call phone number')]/text())").get()
            if phone == "":
                results = respObj.xpath("//div[@id='search']//div[@class='g']")
                for result in results:
                    societe = result.xpath(".//a[contains(@href, 'www.societe.com')]/@href").get()
                    mappy = result.xpath(".//a[contains(@href, 'fr.mappy.com')]/@href").get()
                    if societe or mappy:                        
                        if societe:                
                            try:
                                driver.switch_to.window(driver.window_handles[1])
                                driver.get(societe)
                                WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), 'Afficher le num')]")))
                                time.sleep(1)
                                driver.find_element_by_xpath("//span[contains(text(), 'Afficher le num')]").click()
                                time.sleep(2)
                                html = driver.page_source
                                respObj = Selector(text=html)
                                phone = respObj.xpath("normalize-space(//strong[@id='telab-rensjur-num']/text())").get()
                                driver.switch_to.window(driver.window_handles[0])
                                break
                            except:
                                phone = None
                                driver.switch_to.window(driver.window_handles[0])
                                break
                        elif mappy:                        
                            try:
                                driver.switch_to.window(driver.window_handles[2])
                                driver.get(mappy)
                                WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//ul[@class='contacts']")))
                                if i == 1:
                                    time.sleep(15)                            
                                else:
                                    time.sleep(3)
                                i += 1    
                                html = driver.page_source
                                respObj = Selector(text=html)
                                phone = respObj.xpath("normalize-space(//ul[@class='contacts']//a[contains(@href, 'tel')]/@href[last()])").get()
                                driver.switch_to.window(driver.window_handles[0])
                                break
                            except:
                                phone = None
                                driver.switch_to.window(driver.window_handles[0])
                                break
                        else:
                            phone = None
                            break

            yield{
                'query': value['Query'],
                'phone': phone
            }