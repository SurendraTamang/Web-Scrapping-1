from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from scrapy import Selector
from selenium_stealth import stealth
import os
import csv
import time


# FILE_NAME = '/content/drive/MyDrive/fiverrWorkspace/marriagesData/photo/PhotoFrance.csv'
FILE_NAME = './MusicSpain.csv'
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

driver.get("https://www.bodas.net/bodas/proveedores/musica")
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
    'Precio',
    'Servicios',
    'Estilos',
    'Qu?? incluye el pack de boda',
    'Con cu??nta antelaci??n debo ponerme en contacto contigo',
    'Tama??o de la formaci??n',
    'Repertorio',
    'Existe alg??n problema o impedimento si solicito un tema que no est?? en el repertorio',
    'Experiencia',
    'Dispones de equipo propio',
    'Necesitas alg??n material en concreto o condiciones espec??ficas para poder ofrecer tus servicios',
    'Tienes posibilidad de desplazarte',
    'Existe alg??n cargo por desplazamiento',
    'Cubres m??s de una boda al d??a',
    'Trabajas solo o cuentas con un equipo de profesionales',
    'Cu??nto tiempo dura la actuaci??n',
    'Cu??nto tiempo necesitas para preparar la actuaci??n',
    'Realizas actuaciones al aire libre',
    'Cobras por horas o por evento',
    'Si fuese necesario podr??as trabajar horas extra',
    'C??mo cobras las horas extra',
    'C??mo se efect??a el pago',
    'Base Url'
  ]
  prem = respObj.xpath("//h1/following-sibling::i/@class").get()
  try:
    if "premium" in prem:
        prem = "Premium"
  except:
    pass
  quel1 = respObj.xpath("//span[contains(text(), 'Tama??o de la formaci??n')]/parent::li/div/div/div/text()").getall()
  data = {
      FIELD_NAMES[0]: respObj.xpath("normalize-space(//h1/text())").get(),
      FIELD_NAMES[1]: prem,
      FIELD_NAMES[2]: respObj.xpath("normalize-space((//div[contains(@class, 'address')]/text())[2])").get(),
      FIELD_NAMES[3]: respObj.xpath("normalize-space(//div[@class='storefrontAddresses__content']/text())").get().split(" ")[-1],
      FIELD_NAMES[4]: f'''{respObj.xpath("normalize-space(//i[contains(@class, 'phone')]/parent::p/text()[last()])").get()}''',
      FIELD_NAMES[5]: respObj.xpath("normalize-space(//ul[@class='breadcrumb']/li[4]/a/text())").get(),
      FIELD_NAMES[6]: respObj.xpath("normalize-space(//ul[@class='breadcrumb']/li[5]/a/text())").get(),
      FIELD_NAMES[7]: respObj.xpath("normalize-space(//span[contains(text(), 'Precio')]/following-sibling::span/text())").get(),
      FIELD_NAMES[8]: f'''{respObj.xpath("normalize-space(//span[text()='Servicios']/parent::div/text()[2])").get()}{respObj.xpath("normalize-space((//span[text()='Servicios']/parent::div/span[@style]/text())[last()])").get()}''',
      FIELD_NAMES[9]: f'''{respObj.xpath("normalize-space(//span[text()='Estilos']/parent::div/text()[2])").get()}{respObj.xpath("normalize-space((//span[text()='Estilos']/parent::div/span[@style]/text())[last()])").get()}''',
      FIELD_NAMES[10]: respObj.xpath("normalize-space(//span[contains(text(), 'Qu?? incluye el pack de boda')]/parent::li/div/text())").get(),
      FIELD_NAMES[11]: respObj.xpath("normalize-space(//span[contains(text(), 'Con cu??nta antelaci??n debo ponerme en contacto contigo')]/parent::li/div/text())").get(),
      FIELD_NAMES[12]: ", ".join(i.strip() for i in quel1),          
      FIELD_NAMES[13]: respObj.xpath("normalize-space(//span[contains(text(), 'Repertorio')]/parent::li/div/text())").get(),
      FIELD_NAMES[14]: respObj.xpath("normalize-space(//span[contains(text(), 'Existe alg??n problema o impedimento si solicito un tema que no est?? en el repertorio')]/parent::li/div/text())").get(),
      FIELD_NAMES[15]: respObj.xpath("normalize-space(//span[contains(text(), 'Experiencia')]/parent::li/div/text())").get(),
      FIELD_NAMES[16]: respObj.xpath("normalize-space(//span[contains(text(), 'Dispones de equipo propio')]/parent::li/div/text())").get(),
      FIELD_NAMES[17]: respObj.xpath("normalize-space(//span[contains(text(), 'Necesitas alg??n material en concreto o condiciones espec??ficas para poder ofrecer tus servicios')]/parent::li/div/text())").get(),
      FIELD_NAMES[18]: respObj.xpath("normalize-space(//span[contains(text(), 'Tienes posibilidad de desplazarte')]/parent::li/div/text())").get(),
      FIELD_NAMES[19]: respObj.xpath("normalize-space(//span[contains(text(), 'Existe alg??n cargo por desplazamiento')]/parent::li/div/text())").get(),
      FIELD_NAMES[20]: respObj.xpath("normalize-space(//span[contains(text(), 'Cubres m??s de una boda al d??a')]/parent::li/div/text())").get(),
      FIELD_NAMES[21]: respObj.xpath("normalize-space(//span[contains(text(), 'Trabajas solo o cuentas con un equipo de profesionales')]/parent::li/div/text())").get(),
      FIELD_NAMES[22]: respObj.xpath("normalize-space(//span[contains(text(), 'Cu??nto tiempo dura la actuaci??n')]/parent::li/div/text())").get(),
      FIELD_NAMES[23]: respObj.xpath("normalize-space(//span[contains(text(), 'Cu??nto tiempo necesitas para preparar la actuaci??n')]/parent::li/div/text())").get(),
      FIELD_NAMES[24]: respObj.xpath("normalize-space(//span[contains(text(), 'Realizas actuaciones al aire libre')]/parent::li/div/text())").get(),
      FIELD_NAMES[25]: respObj.xpath("normalize-space(//span[contains(text(), 'Cobras por horas o por evento')]/parent::li/div/text())").get(),
      FIELD_NAMES[26]: respObj.xpath("normalize-space(//span[contains(text(), 'podr??as trabajar horas extra')]/parent::li/div/text())").get(),
      FIELD_NAMES[27]: respObj.xpath("normalize-space(//span[contains(text(), 'C??mo cobras las horas extra')]/parent::li/div/text())").get(),
      FIELD_NAMES[28]: respObj.xpath("normalize-space(//span[contains(text(), 'C??mo se efect??a el pago')]/parent::li/div/text())").get(),
      FIELD_NAMES[29]: driver.current_url,
  }
  # print(data)
  writeCSV(data, FIELD_NAMES, FILE_NAME)
  data.clear()
driver.quit()