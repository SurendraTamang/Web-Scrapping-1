from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from scrapy import Selector
from selenium_stealth import stealth
import os
import csv
import time


FILE_NAME = '/content/drive/MyDrive/fiverrWorkspace/marriagesData/video/VideoItaly.csv'
# FILE_NAME = './PhotoItaly.csv'
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
driver = webdriver.Chrome('../chromedriver',chrome_options=chrome_options)

stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

driver.get("https://www.matrimonio.com/video-matrimonio ")
time.sleep(2)

try:
  cookiesBtnElem = driver.find_element_by_xpath("//button[text()='Accetta']")
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
    'Prezzo',
    'Servizi',
    'Pack matrimonio',
    'Trasferte',
    'Con quanto anticipo mi devo mettere in contatto con te',
    'Lavori per più di un matrimonio al giorno',
    'Qual è il sovrapprezzo in caso di spostamento',
    'Che stile di video realizzi',
    'Quali tipologie di video realizzi',
    'Che tipo di tecnologia utilizzi',
    'Utilizzi qualche tecnica nuova o particolare',
    'Che strumentazione utilizzi',
    'Lavori da solo o con un equipe di professionisti',
    'Ti avvali di collaboratori in caso d imprevisto',
    'Riservi ogni diritto sul video nuziale',
    'All incirca quali sono i tempi di consegna del prodotto finito',
    'Ti fai pagare per ora o per evento',
    'Se fosse necessario saresti disponibile a lavorare delle ore extra',
    'Come ti fai pagare le ore extra',
    'Come si effettua il pagamento',
    'Come lavori',
    'Base Url'
  ]
  prem = respObj.xpath("//h1/following-sibling::i/@class").get()
  try:
    if "premium" in prem:
        prem = "Premium"
  except:
    pass
  quel1 = respObj.xpath("//span[contains(text(), 'Che stile di video realizzi')]/parent::li/div/div/div/text()").getall()
  data = {
      FIELD_NAMES[0]: respObj.xpath("normalize-space(//h1/text())").get(),
      FIELD_NAMES[1]: prem,
      FIELD_NAMES[2]: respObj.xpath("normalize-space((//div[contains(@class, 'address')]/text())[2])").get(),
      FIELD_NAMES[3]: respObj.xpath("normalize-space(//div[@class='storefrontAddresses__content']/text())").get().split(" ")[-1],
      FIELD_NAMES[4]: f'''{respObj.xpath("normalize-space(//i[contains(@class, 'phone')]/parent::p/text()[last()])").get()}''',
      FIELD_NAMES[5]: respObj.xpath("normalize-space(//ul[@class='breadcrumb']/li[3]/a/text())").get(),
      FIELD_NAMES[6]: respObj.xpath("normalize-space(//ul[@class='breadcrumb']/li[4]/a/text())").get(),
      FIELD_NAMES[7]: respObj.xpath("normalize-space(//ul[@class='breadcrumb']/li[5]/a/text())").get(),
      FIELD_NAMES[8]: respObj.xpath("normalize-space(//span[contains(text(), 'Prezzo')]/following-sibling::span/text())").get(),
      FIELD_NAMES[9]: f'''{respObj.xpath("normalize-space(//span[text()='Servizi']/parent::div/text()[2])").get()}{respObj.xpath("normalize-space((//span[text()='Servizi']/parent::div/span[@style]/text())[last()])").get()}''',
      FIELD_NAMES[10]: f'''{respObj.xpath("normalize-space(//span[text()='Pack matrimonio']/parent::div/text()[2])").get()}{respObj.xpath("normalize-space((//span[text()='Pack matrimonio']/parent::div/span[@style]/text())[last()])").get()}''',
      FIELD_NAMES[11]: respObj.xpath("normalize-space(//span[text()='Trasferte']/parent::div/text()[2])").get(),      
      FIELD_NAMES[12]: respObj.xpath("normalize-space(//span[contains(text(), 'Con quanto anticipo mi devo mettere in contatto con te')]/parent::li/div/text())").get(),
      FIELD_NAMES[13]: respObj.xpath("normalize-space(//span[contains(text(), 'Lavori per più di un matrimonio al giorno')]/parent::li/div/text())").get(),
      FIELD_NAMES[14]: respObj.xpath("normalize-space(//span[contains(text(), 'Qual è il sovrapprezzo in caso di spostamento')]/parent::li/div/text())").get(),
      FIELD_NAMES[15]: ", ".join(i.strip() for i in quel1),
      FIELD_NAMES[16]: respObj.xpath("normalize-space(//span[contains(text(), 'Quali tipologie di video realizzi')]/parent::li/div/text())").get(),
      FIELD_NAMES[17]: respObj.xpath("normalize-space(//span[contains(text(), 'Che tipo di tecnologia utilizzi')]/parent::li/div/text())").get(),
      FIELD_NAMES[18]: respObj.xpath("normalize-space(//span[contains(text(), 'Utilizzi qualche tecnica nuova o particolare')]/parent::li/div/text())").get(),
      FIELD_NAMES[19]: respObj.xpath("normalize-space(//span[contains(text(), 'Che strumentazione utilizzi')]/parent::li/div/text())").get(),
      FIELD_NAMES[20]: respObj.xpath("normalize-space(//span[contains(text(), 'Lavori da solo o con un')]/parent::li/div/text())").get(),
      FIELD_NAMES[21]: respObj.xpath("normalize-space(//span[contains(text(), 'Ti avvali di collaboratori in caso d')]/parent::li/div/text())").get(),
      FIELD_NAMES[22]: respObj.xpath("normalize-space(//span[contains(text(), 'Riservi ogni diritto sul video nuziale')]/parent::li/div/text())").get(),
      FIELD_NAMES[23]: respObj.xpath("normalize-space(//span[contains(text(), 'quali sono i tempi di consegna del prodotto finito')]/parent::li/div/text())").get(),
      FIELD_NAMES[24]: respObj.xpath("normalize-space(//span[contains(text(), 'Ti fai pagare per ora o per evento')]/parent::li/div/text())").get(),
      FIELD_NAMES[25]: respObj.xpath("normalize-space(//span[contains(text(), 'saresti disponibile a lavorare delle ore extra')]/parent::li/div/text())").get(),
      FIELD_NAMES[26]: respObj.xpath("normalize-space(//span[contains(text(), 'Come ti fai pagare le ore extra')]/parent::li/div/text())").get(),
      FIELD_NAMES[27]: respObj.xpath("normalize-space(//span[contains(text(), 'Come si effettua il pagamento')]/parent::li/div/text())").get(),
      FIELD_NAMES[28]: respObj.xpath("normalize-space(//span[contains(text(), 'Come lavori')]/parent::li/div/text())").get(),
      FIELD_NAMES[29]: driver.current_url,
  }
  # print(data)
  writeCSV(data, FIELD_NAMES, FILE_NAME)
  data.clear()
driver.quit()