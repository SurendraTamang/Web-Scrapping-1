import scrapy
from scrapy import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import time
import re


class KstrSpider(scrapy.Spider):
    name = 'kstr'

    # df = pd.read_excel("/home/p.byom26/residentialReits/rrScrapers/kickstarter/links.xlsx", sheet_name="gcp")
    df = pd.read_excel("/root/rrScrapers/kickstarter/links_data.xlsx", sheet_name="linode1")
    data = pd.read_excel("/root/rrScrapers/kickstarter/l1FnsdData.xlsx")
    li = data['Title'].values.tolist()
    
    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.kickstarter.com",
            wait_time=10,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        driver.maximize_window()
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[0])
        for _,value in self.df.iterrows():
            cntr = 199
            while True:
                location = value['Location']
                category = value['Category']
                subCat = value['Subcategory']
                url = f"{value['URL']}{cntr}"
                driver.get(url)
                cntr += 1
                WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "(//div[@class='js-project-group'])[2]//h3/parent::a[@class='soft-black mb3']")))
        
                html = driver.page_source
                respObj = Selector(text=html)

                count = respObj.xpath("normalize-space(//b[contains(@class, 'count')]/text())").get()
                pCount = int("".join(re.findall(r'\d+', count)))

                driver.switch_to.window(driver.window_handles[1])
                items = respObj.xpath("(//div[@class='js-project-group'])[2]//h3/parent::a[@class='soft-black mb3']")
                for item in items:
                    title = item.xpath("normalize-space(.//h3/text())").get()
                    if title not in self.li:
                        self.li.append(title)
                        url = item.xpath(".//@href").get()
                        driver.get(url)
                        time.sleep(1)
                        WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//a[@data-modal-title='About the creator']")))
                        html1 = driver.page_source
                        respObj1 = Selector(text=html1)
                        title = respObj1.xpath("normalize-space(//h2/span/a/text())").get()
                        creator = respObj1.xpath("normalize-space(//a[@data-modal-title='About the creator']/text())").get()
                        backers = respObj1.xpath("normalize-space(//b[contains(text(), 'backers')]/text())").get()
                        money = respObj1.xpath("normalize-space(//span[@class='money']/text())").get()
                        driver.find_element_by_xpath("//a[@data-modal-title='About the creator']").click()
                        time.sleep(2)
                        html2 = driver.page_source
                        respObj2 = Selector(text=html2)
                        yield{
                            'Title': title,
                            'Creator': creator,
                            'Backers': backers.replace(" backers", ""),
                            'Money': money,
                            'Website': respObj2.xpath("//h4[contains(text(), 'Websites')]/following-sibling::ul/li/a/@href").getall(),
                            'Location': location,
                            'Category': category,
                            'Sub Category': subCat
                        }
                    else:
                        pass
                driver.switch_to.window(driver.window_handles[0])
                a = pCount//12
                if pCount % 12 != 0:
                    a += 1
                else:
                    a += 0
                if cntr > 200:
                    break
        
