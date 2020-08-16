import scrapy
import time
import pandas as pd
from scrapy import Selector
from selenium.webdriver.common.action_chains import ActionChains
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class AldispiderSpider(scrapy.Spider):
    name = 'aldiSpider'

    df = pd.read_excel("D:/linodeWorkspace/Finished/aldi/aldiProducts.xlsx")

    def scroll(self, driver, timeout):
        scroll_pause_time = timeout

        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(scroll_pause_time)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                # If heights are the same it will exit the function
                break
            last_height = new_height

    def validate_img_url(self, img_url):
        try:
            if "image_coming_soon" in img_url:
                return None
            else:
                return img_url
        except:
            return None

    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.aldi.co.uk/c/groceries/groceriescategories",
            wait_time=5,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        driver.maximize_window()
        # WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "(//ul[contains(@class, 'category-facets')])[last()]")))
        
        # html1 = driver.page_source
        # response1 = Selector(text=html1)

        # categories = response1.xpath("(//ul[contains(@class, 'category-facets')])[last()]/li/div/a")
        
        # driver.execute_script("window.open('');")
        # driver.switch_to.window(driver.window_handles[1])
        
        # for category in categories:
        #     cat_url = f'''https://www.aldi.co.uk{category.xpath(".//@href").get()}'''
        #     driver.get(cat_url)
        #     WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'category-item')]/a")))
        #     self.scroll(driver, 4)
        #     html2 = driver.page_source
        #     response2 = Selector(text=html2)
        #     items = response2.xpath("//div[contains(@class, 'category-item')]/a[1]")
            
            # driver.execute_script("window.open('');")
            # driver.switch_to.window(driver.window_handles[2])
            # for item in items:
            #     item_url = item.xpath(".//@href").get()
            #     yield{
            #         'url': item_url
            #     }

        for _,value in self.df.iterrows():
            try:
                driver.get(value['url'])
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//h1[@class='product-details__name']")))
                html3 = driver.page_source
                response3 = Selector(text=html3)
                lvl3_cat = response3.xpath("normalize-space(//ul[@data-component='breadcrumb']/li[4]/a/text())").get()
                if "Beers and Ciders" not in lvl3_cat:
                    yield {
                        'productName' : response3.xpath("normalize-space(//h1[@class='product-details__name']/text())").get(),
                        'servingSize': response3.xpath("normalize-space(//p[contains(text(), 'Size / Weight:')]/following-sibling::p/text())").get(),
                        'price': response3.xpath("normalize-space(//span[@class='product-price__value']/text())").get(),
                        'imageURL': self.validate_img_url(response3.xpath("//div[contains(@class, 'picture-container')]/@data-original-src").get()),
                        'url' : driver.current_url,
                        'lvl1_cat' : response3.xpath("normalize-space(//ul[@data-component='breadcrumb']/li[2]/a/text())").get(),
                        'lvl2_cat' : response3.xpath("normalize-space(//ul[@data-component='breadcrumb']/li[3]/a/text())").get(),
                        'lvl3_cat' : lvl3_cat
                    }
            except:
                pass
            # driver.close()  
            # driver.switch_to.window(driver.window_handles[1])
        
        # driver.close()  
        # driver.switch_to.window(driver.window_handles[0])
