import scrapy
from scrapy import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd


class SteamSpider(scrapy.Spider):
    name = 'steam'
    cntr = 1
    df = pd.read_csv("dataRaw.csv")
    urlCheck = df['Url'].values.tolist()
    
    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.google.com",
            wait_time=5,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        #driver.switch_to.window(driver.window_handles[0])
        #driver.maximize_window()
        driver.set_window_size(1920, 1080)
        driver.get("https://steamcommunity.com/market/search?appid=730#p46_popular_desc")
        while True:
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='searchResultsRows']")))        
            time.sleep(1)
            html1 = driver.page_source
            resp1 = Selector(text=html1)
            pagination = driver.current_url
            # print(driver.current_url)
            # input()
            results = resp1.xpath("//div[@id='searchResultsRows']/a")
            #driver.set_window_size(1920, 1080)
            for result in results:
                if result.xpath(".//@href").get() not in self.urlCheck:
                    self.urlCheck.append(result.xpath(".//@href").get())
                    driver.execute_script("window.open('');")
                    driver.switch_to.window(driver.window_handles[1])
                    driver.get(result.xpath(".//@href").get())
                    while True:
                        try:
                            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'description')]")))
                            break
                        except:
                            time.sleep(60)
                            driver.refresh()
                    time.sleep(1)
                    html2 = driver.page_source
                    resp2 = Selector(text=html2)
                    lso = resp2.xpath("normalize-space(//div[contains(text(), 'sale starting')]/span[last()]/text())").get()
                    hbo = resp2.xpath("normalize-space(//div[contains(text(), 'to buy')]/span[last()]/text())").get()
                    if not lso:
                        prices = resp2.xpath("//div[@id='searchResultsRows']/div[contains(@id, 'listing')]")
                        for price in prices:
                            lso = price.xpath("normalize-space(.//span[contains(@class,'price_with_fee')]/text())").get()
                            if any(map(str.isdigit, lso)):
                                break
                            else:
                                pass

                    yield {
                        'Name': resp2.xpath("normalize-space(//div[contains(@class, 'description')]/h1/text())").get(),
                        'Heighest Buy Order': hbo,
                        'Lowest Selling Order': lso,
                        'Url': driver.current_url,
                        'Pagination': pagination
                    }
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    #time.sleep(6)
            nextPage = resp1.xpath("//span[@id='searchResults_btn_next']/@class").get()
            if "disabled" in nextPage or "#p801" in pagination:
                break
            else:
                self.cntr += 1
                elem = driver.find_element_by_xpath("//span[@id='searchResults_btn_next']")
                driver.execute_script("arguments[0].click()", elem)
                # driver.find_element_by_xpath("//span[@id='searchResults_btn_next']").click()
                time.sleep(5)
                # if self.cntr % 5 == 0:
                #     driver.refresh()
