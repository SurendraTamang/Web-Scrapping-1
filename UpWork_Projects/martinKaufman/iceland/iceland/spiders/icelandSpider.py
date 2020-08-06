import scrapy
import time
from scrapy import Selector
from selenium.webdriver.common.action_chains import ActionChains
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class IcelandspiderSpider(scrapy.Spider):
    name = 'icelandSpider'
    
    categoryURLs = [
        'https://www.iceland.co.uk/frozen',
        'https://www.iceland.co.uk/fresh',
        'https://www.iceland.co.uk/food-cupboard',
        'https://www.iceland.co.uk/drinks',
        'https://www.iceland.co.uk/bakery'
    ]

    def extractServingSize(self, value):
        try:
            li = value.split(" ")
            if li[-1:] == ['kg'] or li[-1:] == ['ml']:
                return "".join(str(i) for i in li[-2:])
            else:
                return li[-1:]
        except:
            return None
    
    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.iceland.co.uk",
            wait_time=5,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        driver.maximize_window()
        for categoryURL in self.categoryURLs:
            driver.get(categoryURL)
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//ul[contains(@class, 'search-result-items')]/li")))
            time.sleep(1)

            while True:
                html1 = driver.page_source
                response1 = Selector(text=html1)

                productURLs = response1.xpath("//ul[contains(@class, 'search-result-items')]/li")
                
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[1])

                for productURL in productURLs:
                    url = productURL.xpath(".//a[@class='name-link']/@href").get()
                    driver.get(url)
                    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='product-price']/span")))
                    html2 = driver.page_source
                    response2 = Selector(text=html2)
                    productName = response2.xpath("normalize-space(//h2[@class='product-name']/text())").get()
                    caloriesPER100g = response2.xpath("normalize-space(//td[text()=' kcal' or text()='Energy (kcal)']/following-sibling::td/text())").get()
                    if not caloriesPER100g:
                        caloriesPER100g = response2.xpath("normalize-space(//td[text()='Energy']/following-sibling::td/text()[2])").get()
                    yield{
                        'productName' : productName,
                        'servingSize': self.extractServingSize(productName),
                        'caloriesPER100g': caloriesPER100g,
                        'price': response2.xpath("normalize-space(//div[@class='product-price']/span/span/text())").get(),
                        'imageURL': response2.xpath("//img[@class='primary-image']/parent::a/@href").get(),
                        'url' : driver.current_url,
                        'lvl1_cat' : response2.xpath("normalize-space(//ol[contains(@class, 'breadcrumb')]/li[1]/a/text())").get(),
                        'lvl2_cat' : response2.xpath("normalize-space(//ol[contains(@class, 'breadcrumb')]/li[2]/a/text())").get(),
                        'lvl3_cat' : response2.xpath("normalize-space(//ol[contains(@class, 'breadcrumb')]/li[3]/a/text())").get()
                    }
                
                driver.close()  
                driver.switch_to.window(driver.window_handles[0])

                nextPage = response1.xpath("//a[@title='Go to next page']")
                if nextPage:
                    driver.find_element_by_xpath("//a[@title='Go to next page']").click()
                    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//ul[contains(@class, 'search-result-items')]/li")))
                    time.sleep(1)
                else:
                    break
