import scrapy
import time
from scrapy import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd


class IherbSpider(scrapy.Spider):
    name = 'iherb'

    df = pd.read_excel("D:/sipun/Web-Scrapping/UpWork_Projects/kacper/iherbDotCom/urlCheck.xlsx")
    urls = df['url'].to_list()

    def check_br(self, val):
        try:
            if val.endswith('<br>'):
                return val.rstrip(">").rstrip("<br")
            else:
                return val
        except:
            return val

    def start_requests(self):
        yield SeleniumRequest(
            # url="https://www.iherb.com/c/supplements?noi=48",
            # url="https://www.iherb.com/c/Bath-Personal-Care?noi=48",
            # url="https://www.iherb.com/c/Beauty?noi=48",
            # url="https://www.iherb.com/c/Sports-Nutrition?noi=48",
            # url="https://www.iherb.com/c/Bath-Personal-Care?noi=48",
            url="https://www.iherb.com/c/Grocery?noi=48",
            wait_time=5,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        driver.maximize_window()
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[0])
        # WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'language-select')]"))).click()
        # WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "(//div[@class='country-column'])[2]//i"))).click()
        # WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "(//div[@class='country-column'])[2]//div[@data-val='pt-BR']"))).click()
        # WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//button[text()='Guardar preferĂȘncias']"))).click()
        # WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//button[text()='Guardar preferĂȘncias']"))).click()
        # time.sleep(60)
        input()
        WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='pagination']")))

        while True:
            html1 = driver.page_source
            respObj1 = Selector(text=html1)
            
            driver.switch_to.window(driver.window_handles[1])
            products = respObj1.xpath("//div[@class='products clearfix']/div//a[contains(@class, 'product-link')]")
            for product in products:
                if product.xpath(".//@href").get() not in self.urls:
                    bc = []
                    driver.get(product.xpath(".//@href").get())
                    try:
                        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='thumbnail-container']/img")))
                    except:
                        pass
                    html2 = driver.page_source
                    respObj2 = Selector(text=html2)
                    if not respObj2.xpath("//p[contains(text(), 'Este produto nĂŁo estĂĄ disponĂ­vel')]"):
                        breadCrumbs = respObj2.xpath("//a[text()='Categorias']/following-sibling::a")
                        prodImages = respObj2.xpath("//div[@class='thumbnail-container']/img/@data-large-img").getall()
                        if len(prodImages) > 3:
                            pimgStr = ",".join(prodImages[:3])
                        elif len(prodImages) >= 1 and len(prodImages) <= 3:
                            pimgStr = ",".join(prodImages)
                        else:
                            pimgStr = respObj2.xpath("//div[@id='product-image']//a/@href").get()
                        for val in breadCrumbs:
                            bcValue = val.xpath("normalize-space(.//text())").get()
                            if bcValue == "Categorias":
                                break
                            else:
                                bc.append(bcValue)
                        try:
                            wrngi = self.check_br(respObj2.xpath("//strong[text()='AdvertĂȘncias']/parent::h3/following-sibling::div").get()[:-6]).replace('''<div class="prodOverviewDetail">''',"").strip()
                            wrng = wrngi.replace("\n", "")
                        except:
                            wrng = None
                        try:
                            otherIngi = self.check_br(respObj2.xpath("//strong[text()='Outros Ingredientes']/parent::h3/following-sibling::div").get()[:-6]).replace('''<div class="prodOverviewIngred">''',"").strip()
                            otherIng = otherIngi.replace("\n", "")
                        except:
                            otherIng = None
                        try:
                            descpti = self.check_br(respObj2.xpath("//strong[text()='DescriĂ§ĂŁo']/parent::h3/following-sibling::div").get()[:-6]).replace('''<div itemprop="description">''',"").strip()
                            descpt = descpti.replace("\n", "")
                        except:
                            descpt = None
                        np = respObj2.xpath("normalize-space((//div[@class='product-grouping-row'])[last()]/div/div[contains(@class, 'attribute-tile')][1]//span[contains(@class, 'price')]/bdi/text())").get()
                        bvp = respObj2.xpath("normalize-space((//div[@class='product-grouping-row'])[last()]/div/div[contains(@class, 'attribute-tile')][2]//span[contains(@class, 'price')]/bdi/text())").get()
                        if (np == "" and bvp == "") or (np == None and bvp == None):
                            np = respObj2.xpath("normalize-space(//div[@class='product-action-container']//div[contains(text(), 'Nosso preĂ§o')]/following-sibling::div[@id='price']/text())").get()
                            bvp = respObj2.xpath("normalize-space(//section[contains(@id,'price')]//b/text())").get()
                        try:
                            expDt = respObj2.xpath("//li[contains(text(), 'Data de validade')]/text()").getall()[1].strip()
                        except:
                            expDt = None
                        yield{
                            'Product Name': respObj2.xpath("normalize-space(//h1[@id='name']/text())").get().replace("\xa0","").strip(),
                            'Product Image URL': pimgStr,
                            'Expiry Date': expDt,
                            'Shipping Weight': respObj2.xpath("normalize-space(//span[@class='product-weight']/text())").get(),
                            'Product Code': respObj2.xpath("normalize-space(//span[@itemprop='sku']/text())").get(),
                            'UPC Code': respObj2.xpath("normalize-space(//li[contains(text(), 'UPC')]/span/text())").get(),
                            'Dimensions': f'''{respObj2.xpath("normalize-space(//span[@id='dimensions']/text())").get()},{respObj2.xpath("normalize-space(//span[@id='actual-weight']/text())").get()}''',
                            'Package Quantity': respObj2.xpath("normalize-space(//li[contains(text(), 'Quantidade')]/text())").get().replace("Quantidade:","").strip(),
                            'Brand Name': respObj2.xpath("normalize-space(//span[@itemprop='name']/bdi/text())").get(),
                            'Normal Quantity': respObj2.xpath("normalize-space((//div[@class='product-grouping-row'])[last()]/div/div[contains(@class, 'attribute-tile')][1]//div[@class='attribute-name']/text())").get(),
                            'Normal Price': np,
                            'Best Value Quantity': respObj2.xpath("normalize-space((//div[@class='product-grouping-row'])[last()]/div/div[contains(@class, 'attribute-tile')][2]//div[@class='attribute-name']/text())").get(),
                            'Best Value price': bvp,
                            'Breadcrumbs': f'''{respObj2.xpath("normalize-space(//a[text()='Categorias']/text())").get()},{",".join(bc)}''',
                            'Warning': wrng,
                            'Other Ingrediants': otherIng,
                            'Description': descpt,
                            'Product url': product.xpath(".//@href").get(),
                        }
                    else:
                        yield{
                            'Product Name': None,
                            'Product Image URL': None,
                            'Expiry Date': None,
                            'Shipping Weight': None,
                            'Product Code': None,
                            'UPC Code': None,
                            'Dimensions': None,
                            'Package Quantity': None,
                            'Brand Name': None,
                            'Normal Quantity': None,
                            'Normal Price': None,
                            'Best Value Quantity': None,
                            'Best Value price': None,
                            'Breadcrumbs': None,
                            'Warning': None,
                            'Other Ingrediants': None,
                            'Description': None,
                            'Product url': product.xpath(".//@href").get(),
                        }
            driver.switch_to.window(driver.window_handles[0])
            nextPage = respObj1.xpath("//a[@class='pagination-next']/@href").get()
            if nextPage:
                print(f'CURRENT PAGE: {nextPage}')
                driver.get(f'https://www.iherb.com{nextPage}')
                WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='pagination']")))
                time.sleep(1)
            else:
                break

