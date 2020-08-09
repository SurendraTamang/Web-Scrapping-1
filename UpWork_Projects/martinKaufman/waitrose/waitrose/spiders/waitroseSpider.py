# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class WaitrosespiderSpider(scrapy.Spider):
    name = 'waitroseSpider'
    
    urls = [
        'https://www.waitrose.com/ecom/shop/browse/groceries/summer',
        'https://www.waitrose.com/ecom/shop/browse/groceries/fresh_and_chilled',
        'https://www.waitrose.com/ecom/shop/browse/groceries/bakery',
        'https://www.waitrose.com/ecom/shop/browse/groceries/frozen',
        'https://www.waitrose.com/ecom/shop/browse/groceries/food_cupboard',
        'https://www.waitrose.com/ecom/shop/browse/groceries/tea_coffee_and_soft_drinks'
    ]

    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.waitrose.com",
            wait_time=5,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        driver.maximize_window()
        for url in self.urls:
            driver.get(url)
            time.sleep(8)
            try:
                driver.find_element_by_xpath("//button[text()='Yes, allow all']").click()
                time.sleep(2)
            except:
                pass
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//ul[@id='subcategoryList']/li")))
            
            html1 = driver.page_source
            response1 = Selector(text=html1)

            subCatURLs1 = response1.xpath("//ul[@id='subcategoryList']/li")

            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])
            for subCatURL1 in subCatURLs1:
                url = f'''https://www.waitrose.com{subCatURL1.xpath(".//a/@href").get()}'''
                driver.get(url)
                WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[@data-test='product-list']/div/div/article")))
                while True:
                    time.sleep(3)
                    #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    html2 = driver.page_source
                    response2 = Selector(text=html2)
                    if response2.xpath("//button[@aria-label='Load more']"):
                        driver.find_element_by_xpath("//button[@aria-label='Load more']").click()
                        #time.sleep(3)
                    else:
                        break
                html3 = driver.page_source
                response3 = Selector(text=html3)
                productURLs = response3.xpath("//div[@data-test='product-list']/div/div/article")
                for productURL in productURLs:
                    yield scrapy.Request(
                        url = f'''https://www.waitrose.com{productURL.xpath(".//header/a/@href").get()}''',
                        callback=self.productDetails
                    )
                    # yield{
                    #     'url': f'''https://www.waitrose.com{productURL.xpath(".//header/a/@href").get()}'''
                    # }
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

    def productDetails(self, response):
        calories = response.xpath("//tbody/tr[2]/td/text()").get()
        ssize = response.xpath("//table/thead/tr/td/text()").get()
        name = response.xpath("//h1/span[@itemprop='name']/text()").get()
        quantity = response.xpath("//h1/span[contains(@class, 'size')]/text()").get()
        lvl1Cat = response.xpath("normalize-space(//ul[contains(@class, 'crumbs')]/li[3]/a/text())").get()
        if lvl1Cat == "Beer, Wine & Spirits" or lvl1Cat == "Kitchen, Dining & Home" or lvl1Cat == "Household":
            pass
        else:
            yield {
                'Name of Food Item': name,
                'Serving Size of Food Item': ssize,
                'Price': response.xpath("normalize-space(//span[@data-test='product-pod-price']/span/text())").get(),
                'Number of Calories Per Serving': calories,
                'Image (link)': response.xpath("//img[@itemprop='image']/@src").get(),
                'Product (link)': response.url,
                'Quantity': quantity,
                'Lvl1 Category': lvl1Cat,
                'Lvl2 Category': response.xpath("normalize-space(//ul[contains(@class, 'crumbs')]/li[4]/a/text())").get(),
                'Lvl3 Category': response.xpath("normalize-space(//ul[contains(@class, 'crumbs')]/li[5]/a/text())").get()
            }