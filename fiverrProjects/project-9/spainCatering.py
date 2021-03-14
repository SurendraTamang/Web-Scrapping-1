from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from scrapy import Selector
from selenium_stealth import stealth
import os
import csv
import time


FILE_NAME = '/content/drive/MyDrive/fiverrWorkspace/marriagesData/catering/CateringSpain.csv'
# FILE_NAME = './FlowersSpain.csv'
urlList = []
pageCntr = 1

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

driver.get("https://www.bodas.net/bodas/banquetes/catering")
time.sleep(2)

try:
  cookiesBtnElem = driver.find_element_by_xpath("//button[text()='Accepter']")
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

  FIELD_NAMES = [
    'Name',
    'Type',
    'Address',
    'Zip Code',
    'Phone',
    'Lvl 1 Category',
    'Lvl 2 Category',
    'Lvl 3 Category',
    'Menús a partir de',
    'Nº de invitados',
    'Servicios',
    'Existe un pedido mínimo',
    'Dispones de fincas donde celebrar el banquete',
    'Cocinas en el mismo lugar del banquete',
    'Qué incluye el menú',
    'Es posible adaptar o modificar los menús',
    'Es posible elaborar menús personalizados',
    'Qué tipo de cocina sirves',
    'Dispones de menús especiales',
    'Cómo funciona la barra libre',
    'Sirves también la tarta de boda',
    'Puedo llevar mi propia tarta de boda Tiene algún recargo',
    'Tienes límite de hora en las celebraciones',
    'Exclusividad fotógrafo',
    'Exclusividad música',
    'Celebras más de un evento al día',
    'Cuál es el recargo en caso de no llegar al mínimo de invitados',
    'Cómo se efectúa el pago',
    'Base Url'
  ]
  prem = respObj.xpath("//h1/following-sibling::i/@class").get()
  try:
    if "premium" in prem:
        prem = "Premium"
  except:
    pass
  quel1 = respObj.xpath("//span[contains(text(), 'Qué tipo de cocina sirves')]/parent::li/div/div/div/text()").getall()
  quel2 = respObj.xpath("//span[contains(text(), 'Dispones de menús especiales')]/parent::li/div/div/div/text()").getall()
  quel3 = respObj.xpath("//span[contains(text(), 'Cómo funciona la barra libre')]/parent::li/div/div/div/text()").getall()
  data = {
      FIELD_NAMES[0]: respObj.xpath("normalize-space(//h1/text())").get(),
      FIELD_NAMES[1]: prem,
      FIELD_NAMES[2]: respObj.xpath("normalize-space((//div[contains(@class, 'address')]/text())[2])").get(),
      FIELD_NAMES[3]: respObj.xpath("normalize-space(//div[@class='storefrontAddresses__content']/text())").get().split(" ")[-1],
      FIELD_NAMES[4]: f'''{respObj.xpath("normalize-space(//i[contains(@class, 'phone')]/parent::p/text()[last()])").get()}''',
      FIELD_NAMES[5]: respObj.xpath("normalize-space(//ul[@class='breadcrumb']/li[3]/a/text())").get(),
      FIELD_NAMES[6]: respObj.xpath("normalize-space(//ul[@class='breadcrumb']/li[4]/a/text())").get(),
      FIELD_NAMES[7]: respObj.xpath("normalize-space(//ul[@class='breadcrumb']/li[5]/a/text())").get(),
      FIELD_NAMES[8]: respObj.xpath("normalize-space(//span[contains(text(), 'Menús')]/following-sibling::span/text())").get(),
      FIELD_NAMES[9]: respObj.xpath("normalize-space(//span[contains(text(), 'Nº de invitados')]/following-sibling::span/text())").get(),
      FIELD_NAMES[10]: f'''{respObj.xpath("normalize-space(//span[text()='Servicios']/parent::div/text()[2])").get()}{respObj.xpath("normalize-space((//span[text()='Servicios']/parent::div/span[@style]/text())[last()])").get()}''',
      FIELD_NAMES[11]: respObj.xpath("normalize-space(//span[contains(text(), 'Existe un pedido mínimo')]/parent::li/div/text())").get(),
      FIELD_NAMES[12]: respObj.xpath("normalize-space(//span[contains(text(), 'Dispones de fincas donde celebrar el banquete')]/parent::li/div/text())").get(),
      FIELD_NAMES[13]: respObj.xpath("normalize-space(//span[contains(text(), 'Cocinas en el mismo lugar del banquete')]/parent::li/div/text())").get(),
      FIELD_NAMES[14]: respObj.xpath("normalize-space(//span[contains(text(), 'Qué incluye el menú')]/parent::li/div/text())").get(),
      FIELD_NAMES[15]: respObj.xpath("normalize-space(//span[contains(text(), 'Es posible adaptar o modificar los menús')]/parent::li/div/text())").get(),
      FIELD_NAMES[16]: respObj.xpath("normalize-space(//span[contains(text(), 'Es posible elaborar menús personalizados')]/parent::li/div/text())").get(),
      FIELD_NAMES[17]: ", ".join(i.strip() for i in quel1), 
      FIELD_NAMES[18]: ", ".join(i.strip() for i in quel2), 
      FIELD_NAMES[19]: ", ".join(i.strip() for i in quel3),       
      FIELD_NAMES[20]: respObj.xpath("normalize-space(//span[contains(text(), 'Sirves también la tarta de boda')]/parent::li/div/text())").get(),
      FIELD_NAMES[21]: respObj.xpath("normalize-space(//span[contains(text(), 'Puedo llevar mi propia tarta de boda')]/parent::li/div/text())").get(),
      FIELD_NAMES[22]: respObj.xpath("normalize-space(//span[contains(text(), 'Tienes límite de hora en las celebraciones')]/parent::li/div/text())").get(),
      FIELD_NAMES[23]: respObj.xpath("normalize-space(//span[contains(text(), 'Exclusividad fotógrafo')]/parent::li/div/text())").get(),
      FIELD_NAMES[24]: respObj.xpath("normalize-space(//span[contains(text(), 'Exclusividad música')]/parent::li/div/text())").get(),
      FIELD_NAMES[25]: respObj.xpath("normalize-space(//span[contains(text(), 'Celebras más de un evento al día')]/parent::li/div/text())").get(),
      FIELD_NAMES[26]: respObj.xpath("normalize-space(//span[contains(text(), 'Cuál es el recargo en caso de no llegar al mínimo de invitados')]/parent::li/div/text())").get(),
      FIELD_NAMES[27]: respObj.xpath("normalize-space(//span[contains(text(), 'Cómo se efectúa el pago')]/parent::li/div/text())").get(),
      FIELD_NAMES[28]: driver.current_url,
  }
  # print(data)
  writeCSV(data, FIELD_NAMES, FILE_NAME)
  data.clear()
driver.quit()