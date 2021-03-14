from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from scrapy import Selector
from selenium_stealth import stealth
import os
import csv
import time


FIELD_NAMES = ['Name', 'Type', 'Address', 'Phone', 'Website Url', 'Lvl 1 Category', 'Lvl 2 Category', 'Lvl 3 Category','Price From', 'Source Url']
# BASE_URLS = ['https://www.hitched.co.uk/wedding-photographers','https://www.hitched.co.uk/wedding-beauty-hair-make-up', 'https://www.hitched.co.uk/wedding-florist', 'https://www.hitched.co.uk/wedding-music-and-djs', 'https://www.hitched.co.uk/wedding-planner']
BASE_URLS = ['https://www.hitched.co.uk/wedding-videographers']

def writeCSV(data, fieldName, FILE_NAME):
    fileExists = os.path.isfile(FILE_NAME)
    with open(FILE_NAME, 'a', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldName, lineterminator='\n')
        if not fileExists:
            writer.writeheader()
        writer.writerow(data)

chrome_options = webdriver.ChromeOptions()
# prefs = {"download.default_directory" : "/some/path"}
# chromeOptions.add_experimental_option("prefs",prefs)
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)

stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

for baseUrl in BASE_URLS:
  urlList = []
  pageCntr = 1
  driver.get(baseUrl)
  time.sleep(2)

  try:
    cookiesBtnElem = driver.find_element_by_xpath("//button[text()='Accept']")
    driver.execute_script("arguments[0].click()", cookiesBtnElem)
    time.sleep(1)
  except:
    pass

  while True:
    pageCntr += 1
    html = driver.page_source
    respObj = Selector(text=html)

    #if pageCntr > 27:
    cards = respObj.xpath("//div[@data-list-type='Catalog']/div[@id]")
    for card in cards:
      urlList.append(card.xpath(".//a[contains(@id, 'app_lnk')]/@href").get())

    nextPageType1 = respObj.xpath(f"//a[@data-page and text()='{pageCntr}']")
    nextPageType2 = respObj.xpath(f"//span[contains(@class, 'pagination') and text()='{pageCntr}']")
    
    if nextPageType1:
      nextBtnElem = driver.find_element_by_xpath(f"//a[@data-page and text()='{pageCntr}']")
      driver.execute_script("arguments[0].click()", nextBtnElem)
      time.sleep(2)
      print(f"\n\n PAGE-{pageCntr}")
    elif nextPageType2:
      nextBtnElem = driver.find_element_by_xpath(f"//span[contains(@class, 'pagination') and text()='{pageCntr}']")
      driver.execute_script("arguments[0].click()", nextBtnElem)
      time.sleep(2)
      print(f"\n\n PAGE-{pageCntr}")
    else:
      break

  for url in urlList:
    driver.get(url)
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//h1")))

    try:
      phoneBtnElem = driver.find_element_by_xpath("//span[@class='app-emp-phone-txt']")
      driver.execute_script("arguments[0].click()", phoneBtnElem)
      WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, "//i[contains(@class, 'phone')]/parent::p")))
    except:
      pass

    html = driver.page_source
    respObj = Selector(text=html)
    
    prem = respObj.xpath("//h1/following-sibling::i/@class").get()
    try:
      if "premium" in prem:
        prem = "Premium"
    except:
      pass
    
    data = {
        FIELD_NAMES[0]: respObj.xpath("normalize-space(//h1/text())").get(),
        FIELD_NAMES[1]: prem,
        FIELD_NAMES[2]: respObj.xpath("normalize-space((//div[contains(@class, 'address')]/text())[2])").get(),
        FIELD_NAMES[3]: f'''{respObj.xpath("normalize-space(//i[contains(@class, 'phone')]/parent::p/text()[last()])").get()}''',      
        FIELD_NAMES[4]: respObj.xpath("//span[contains(text(), 'Website')]/@data-url").get(),
        FIELD_NAMES[5]: respObj.xpath("normalize-space(//ul[@class='breadcrumb']/li[3]/a/text())").get(),
        FIELD_NAMES[6]: respObj.xpath("normalize-space(//ul[@class='breadcrumb']/li[4]/a/text())").get(),
        FIELD_NAMES[7]: respObj.xpath("normalize-space(//ul[@class='breadcrumb']/li[5]/a/text())").get(),
        FIELD_NAMES[8]: respObj.xpath('''normalize-space(//span[contains(text(), 'Price') or contains(text(), 'price')]/parent::div/text()[last()])''').get(),
        FIELD_NAMES[9]: driver.current_url
    }
    print(data)
    writeCSV(data, FIELD_NAMES, f'''/content/drive/MyDrive/uk/{baseUrl.split("/")[-1].strip()}.csv''')
    data.clear()

driver.quit()
