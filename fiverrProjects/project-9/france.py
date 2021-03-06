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
FILE_NAME = './PhotoFrance.csv'
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

driver.get("https://www.mariages.net/photo-mariage")
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
    'Phone',
    'Lvl 1 Category',
    'Lvl 2 Category',
    'Lvl 3 Category',
    'Prix',
    'Services',
    'Formule mariage',
    'Mobilit??',
    'Combien de temps ?? l avance dois-je vous contacter',
    'Couvrez-vous plus d un mariage par jour',
    'Facturez-vous les d??placements',
    'Quels styles de photos r??alisez-vous',
    'Quelles techniques proposez-vous',
    'Utilisez-vous une technique particuli??re ou novatrice',
    'Quel type de mat??riel utilisez-vous',
    'Disposez-vous d une plateforme pour partager les photos en ligne',
    'Quel est le temps aproximatif de livraison du reportage final',
    'Livrez-vous l ensemble des copies originales',
    'Travaillez-vous seul ou en ??quipe',
    'Avez-vous un rempla??ant en cas d emp??chement',
    'Vous r??servez-vous le droit de publier les photographies du mariage',
    'Facturez-vous par heure ou par ??v??nement',
    'Si besoin est accepteriez-vous de faire des heures suppl??mentaires',
    'Quel est le tarif des heures suppl??mentaires',
    'Comment s effectue le paiement',
    'Quelle m??thode de travail utilisez-vous',
    'Base Url'
  ]
  prem = respObj.xpath("//h1/following-sibling::i/@class").get()
  try:
    if "premium" in prem:
        prem = "Premium"
  except:
    pass
  quelsStyle = respObj.xpath("//span[contains(text(), 'Quels styles de photos r??alisez-vous')]/parent::li/div/div/div/text()").getall()
  quelsTechnique = respObj.xpath("//span[contains(text(), 'Quelles techniques proposez-vous')]/parent::li/div/div/div/text()").getall()
  data = {
      FIELD_NAMES[0]: respObj.xpath("normalize-space(//h1/text())").get(),
      FIELD_NAMES[1]: prem,
      FIELD_NAMES[2]: respObj.xpath("normalize-space((//div[contains(@class, 'address')]/text())[2])").get(),
      FIELD_NAMES[3]: f'''{respObj.xpath("normalize-space(//i[contains(@class, 'phone')]/parent::p/text()[last()])").get()}''',
      FIELD_NAMES[4]: respObj.xpath("normalize-space(//ul[@class='breadcrumb']/li[3]/a/text())").get(),
      FIELD_NAMES[5]: respObj.xpath("normalize-space(//ul[@class='breadcrumb']/li[4]/a/text())").get(),
      FIELD_NAMES[6]: respObj.xpath("normalize-space(//ul[@class='breadcrumb']/li[5]/a/text())").get(),
      FIELD_NAMES[7]: respObj.xpath("normalize-space(//span[contains(text(), 'Prix')]/following-sibling::span/text())").get(),
      FIELD_NAMES[8]: f'''{respObj.xpath("normalize-space(//span[text()='Services']/parent::div/text()[2])").get()}{respObj.xpath("normalize-space((//span[text()='Services']/parent::div/span[@style]/text())[last()])").get()}''',
      FIELD_NAMES[9]: f'''{respObj.xpath("normalize-space(//span[text()='Formule mariage']/parent::div/text()[2])").get()}{respObj.xpath("normalize-space((//span[text()='Formule mariage']/parent::div/span[@style]/text())[last()])").get()}''',
      FIELD_NAMES[10]: f'''{respObj.xpath("normalize-space(//span[text()='Mobilit??']/parent::div/text()[2])").get()}{respObj.xpath("normalize-space((//span[text()='Mobilit??']/parent::div/span[@style]/text())[last()])").get()}''',
      FIELD_NAMES[11]: respObj.xpath("normalize-space(//span[contains(text(), 'avance dois-je vous contacter')]/parent::li/div/text())").get(),
      FIELD_NAMES[12]: respObj.xpath("normalize-space(//span[contains(text(), 'un mariage par jour')]/parent::li/div/text())").get(),
      FIELD_NAMES[13]: respObj.xpath("normalize-space(//span[contains(text(), 'Facturez-vous les d??placements')]/parent::li/div/text())").get(),
      FIELD_NAMES[14]: ", ".join(i.strip() for i in quelsStyle),     
      FIELD_NAMES[15]: ", ".join(i.strip() for i in quelsTechnique),     
      FIELD_NAMES[16]: respObj.xpath("normalize-space(//span[contains(text(), 'Utilisez-vous une technique particuli??re ou novatrice')]/parent::li/div/text())").get(),
      FIELD_NAMES[17]: respObj.xpath("normalize-space(//span[contains(text(), 'Quel type de mat??riel utilisez-vous')]/parent::li/div/text())").get(),
      FIELD_NAMES[18]: respObj.xpath("normalize-space(//span[contains(text(), 'une plateforme pour partager les photos en ligne')]/parent::li/div/text())").get(),
      FIELD_NAMES[19]: respObj.xpath("normalize-space(//span[contains(text(), 'Quel est le temps aproximatif de livraison du reportage final')]/parent::li/div/text())").get(),
      FIELD_NAMES[20]: respObj.xpath("normalize-space(//span[contains(text(), 'ensemble des copies originales')]/parent::li/div/text())").get(),
      FIELD_NAMES[21]: respObj.xpath("normalize-space(//span[contains(text(), 'Travaillez-vous seul ou en ??quipe')]/parent::li/div/text())").get(),
      FIELD_NAMES[22]: respObj.xpath("normalize-space(//span[contains(text(), 'Avez-vous un rempla??ant en cas d')]/parent::li/div/text())").get(),
      FIELD_NAMES[23]: respObj.xpath("normalize-space(//span[contains(text(), 'Vous r??servez-vous le droit de publier les photographies du mariage')]/parent::li/div/text())").get(),
      FIELD_NAMES[24]: respObj.xpath("normalize-space(//span[contains(text(), 'Facturez-vous par heure ou par ??v??nement')]/parent::li/div/text())").get(),
      FIELD_NAMES[25]: respObj.xpath("normalize-space(//span[contains(text(), 'accepteriez-vous de faire des heures suppl??mentaires')]/parent::li/div/text())").get(),
      FIELD_NAMES[26]: respObj.xpath("normalize-space(//span[contains(text(), 'Quel est le tarif des heures suppl??mentaires')]/parent::li/div/text())").get(),
      FIELD_NAMES[27]: respObj.xpath("normalize-space(//span[contains(text(), 'effectue le paiement')]/parent::li/div/text())").get(),
      FIELD_NAMES[28]: respObj.xpath("normalize-space(//span[contains(text(), 'Quelle m??thode de travail utilisez-vous')]/parent::li/div/text())").get(),
      FIELD_NAMES[29]: driver.current_url,
  }
  # print(data)
  writeCSV(data, FIELD_NAMES, FILE_NAME)
  data.clear()
driver.quit()




#--officiants--#
# FIELD_NAMES = [
#   'Name',
#   'Type',
#   'Address',
#   'Phone',
#   'Lvl 1 Category',
#   'Lvl 2 Category',
#   'Lvl 3 Category',
#   'Prix par menu',
#   'Capacit?? mariage',
#   'C??r??monies',
#   'Quels services proposez-vous',
#   'Organisez-vous les mariages religieux non catholiques',
#   'Dans quels types de c??r??monies vous sp??cialisez-vous',
#   'Quelle est votre m??thode de travail',
#   'Comment s effectue le paiement',
#   'Base Url'
# ]
# prem = respObj.xpath("//h1/following-sibling::i/@class").get()
# try:
#   if "premium" in prem:
#       prem = "Premium"
# except:
#   pass
# quelsServices = respObj.xpath("//span[contains(text(), 'Quels services proposez-vous')]/parent::li/div/div/div/text()").getall()
# data = {
#     FIELD_NAMES[0]: respObj.xpath("normalize-space(//h1/text())").get(),
#     FIELD_NAMES[1]: prem,
#     FIELD_NAMES[2]: respObj.xpath("normalize-space((//div[contains(@class, 'address')]/text())[2])").get(),
#     FIELD_NAMES[3]: f'''{respObj.xpath("normalize-space(//i[contains(@class, 'phone')]/parent::p/text()[last()])").get()}''',
#     FIELD_NAMES[4]: respObj.xpath("normalize-space(//ul[@class='breadcrumb']/li[3]/a/text())").get(),
#     FIELD_NAMES[5]: respObj.xpath("normalize-space(//ul[@class='breadcrumb']/li[4]/a/text())").get(),
#     FIELD_NAMES[6]: respObj.xpath("normalize-space(//ul[@class='breadcrumb']/li[5]/a/text())").get(),
#     FIELD_NAMES[7]: respObj.xpath("normalize-space(//span[contains(text(), 'Prix')]/following-sibling::span/text())").get(),
#     FIELD_NAMES[8]: f'''{respObj.xpath("normalize-space(//span[text()='Capacit?? mariage']/parent::div/text()[2])").get()}{respObj.xpath("normalize-space((//span[text()='Capacit?? mariage']/parent::div/span[@style]/text())[last()])").get()}''',
#     FIELD_NAMES[9]: f'''{respObj.xpath("normalize-space(//span[text()='C??r??monies']/parent::div/text()[2])").get()}{respObj.xpath("normalize-space((//span[text()='C??r??monies']/parent::div/span[@style]/text())[last()])").get()}''',
#     FIELD_NAMES[10]: ", ".join(i.strip() for i in quelsServices),      
#     FIELD_NAMES[11]: respObj.xpath("normalize-space(//span[contains(text(), 'Organisez-vous les mariages religieux non catholiques')]/parent::li/div/text())").get(),
#     FIELD_NAMES[12]: respObj.xpath("normalize-space(//span[contains(text(), 'Dans quels types de c??r??monies vous sp??cialisez-vous')]/parent::li/div/text())").get(),
#     FIELD_NAMES[13]: respObj.xpath("normalize-space(//span[contains(text(), 'Quelle est votre m??thode de travail')]/parent::li/div/text())").get(),
#     FIELD_NAMES[14]: respObj.xpath("normalize-space(//span[contains(text(), 'effectue le paiement')]/parent::li/div/text())").get(),
#     FIELD_NAMES[15]: driver.current_url,
# }


#=========================================================================================================================================================================


#--Flower--#
# FIELD_NAMES = [
#   'Name',
#   'Type',
#   'Address',
#   'Phone',
#   'Lvl 1 Category',
#   'Lvl 2 Category',
#   'Lvl 3 Category',
#   'Prix par menu',
#   'Services',
#   'Formule mariage',
#   'Offre services',
#   'Combien de temps ?? l avance dois-je vous contacte',
#   'R??alisez-vous des bouquets de mari??e personnalis??s',
#   'Pouvez-vous vous d??placer',
#   'Facturez-vous les d??placements',
#   'Vous chargez-vous des envois nationaux',
#   'Disposez-vous d un service d aide ?? la d??coration',
#   'Le service d aide ?? la d??coration est-il payant',
#   'Horaire commercial',
#   'Comment s effectue le paiement',
#   'Base Url'
# ]
# prem = respObj.xpath("//h1/following-sibling::i/@class").get()
# try:
#   if "premium" in prem:
#       prem = "Premium"
# except:
#   pass
# tailleDuGroupe = respObj.xpath("//span[contains(text(), 'Taille du groupe')]/parent::li/div/div/div/text()").getall()
# data = {
#     FIELD_NAMES[0]: respObj.xpath("normalize-space(//h1/text())").get(),
#     FIELD_NAMES[1]: prem,
#     FIELD_NAMES[2]: respObj.xpath("normalize-space((//div[contains(@class, 'address')]/text())[2])").get(),
#     FIELD_NAMES[3]: f'''{respObj.xpath("normalize-space(//i[contains(@class, 'phone')]/parent::p/text()[last()])").get()}''',
#     FIELD_NAMES[4]: respObj.xpath("normalize-space(//ul[@class='breadcrumb']/li[3]/a/text())").get(),
#     FIELD_NAMES[5]: respObj.xpath("normalize-space(//ul[@class='breadcrumb']/li[4]/a/text())").get(),
#     FIELD_NAMES[6]: respObj.xpath("normalize-space(//ul[@class='breadcrumb']/li[5]/a/text())").get(),
#     FIELD_NAMES[7]: respObj.xpath("normalize-space(//span[contains(text(), 'Prix')]/following-sibling::span/text())").get(),
#     FIELD_NAMES[8]: f'''{respObj.xpath("normalize-space(//span[text()='Services']/parent::div/text()[2])").get()}{respObj.xpath("normalize-space((//span[text()='Services']/parent::div/span[@style]/text())[last()])").get()}''',
#     FIELD_NAMES[9]: f'''{respObj.xpath("normalize-space(//span[text()='Formule mariage']/parent::div/text()[2])").get()}{respObj.xpath("normalize-space((//span[text()='Formule mariage']/parent::div/span[@style]/text())[last()])").get()}''',
#     FIELD_NAMES[10]: respObj.xpath("normalize-space(//span[text()='Offre services']/following-sibling::p/text())").get(),
#     FIELD_NAMES[11]: respObj.xpath("normalize-space(//span[contains(text(), 'avance dois-je vous contacter')]/parent::li/div/text())").get(),
#     FIELD_NAMES[12]: respObj.xpath("normalize-space(//span[contains(text(), 'R??alisez-vous des bouquets de mari??e personnalis??s')]/parent::li/div/text())").get(),
#     FIELD_NAMES[13]: respObj.xpath("normalize-space(//span[contains(text(), 'Pouvez-vous vous d??placer')]/parent::li/div/text())").get(),
#     FIELD_NAMES[14]: respObj.xpath("normalize-space(//span[contains(text(), 'Facturez-vous les d??placements')]/parent::li/div/text())").get(),
#     FIELD_NAMES[15]: respObj.xpath("normalize-space(//span[contains(text(), 'Vous chargez-vous des envois nationaux')]/parent::li/div/text())").get(),
#     FIELD_NAMES[16]: respObj.xpath("normalize-space(//span[contains(text(), 'Disposez-vous d')]/parent::li/div/text())").get(),
#     FIELD_NAMES[17]: respObj.xpath("normalize-space(//span[contains(text(), 'aide ?? la d??coration est-il payant')]/parent::li/div/text())").get(),
#     FIELD_NAMES[18]: respObj.xpath("normalize-space(//span[contains(text(), 'Horaire commercial')]/parent::li/div/text())").get(),
#     FIELD_NAMES[19]: respObj.xpath("normalize-space(//span[contains(text(), 'effectue le paiement')]/parent::li/div/text())").get(),
#     FIELD_NAMES[20]: driver.current_url,
# }


#=========================================================================================================================================================================


#--Music--#
# FIELD_NAMES = [
#     'Name',
#     'Type',
#     'Address',
#     'Phone',
#     'Lvl 1 Category',
#     'Lvl 2 Category',
#     'Lvl 3 Category',
#     'Prix par menu',
#     'Services',
#     'Styles',
#     'Formation',
#     'Offre services',
#     'Quels sont les services inclus dans le forfait mariage',
#     'Combien de temps ?? l avance dois-je vous contacter',
#     'Taille du groupe',
#     'R??pertoire',
#     'Est-il possible de demander une chanson qui ne figure pas dans le r??pertoire',
#     'Exp??rience',
#     'Disposez-vous de votre propre mat??riel',
#     'Avez-vous besoin de mat??riel sp??cifique ou de conditions particuli??res pour pouvoir travailler',
#     'Pouvez-vous vous d??placer',
#     'Facturez-vous les d??placements',
#     'Couvrez-vous plus d un mariage par jour',
#     'Travaillez-vous seul ou en ??quipe',
#     'Combien de temps dure la prestation',
#     'Combien de temps de pr??paration avez-vous besoin',
#     'Acceptez-vous de travailler en plein air',
#     'Facturez-vous par heure ou par ??v??nement',
#     'accepteriez-vous de faire des heures suppl??mentaires',
#     'Quel est le tarif des heures suppl??mentaires',
#     'Comment s effectue le paiement',
#     'Base Url'
#   ]
# prem = respObj.xpath("//h1/following-sibling::i/@class").get()
# try:
#   if "premium" in prem:
#       prem = "Premium"
# except:
#   pass
# tailleDuGroupe = respObj.xpath("//span[contains(text(), 'Taille du groupe')]/parent::li/div/div/div/text()").getall()
# data = {
#     FIELD_NAMES[0]: respObj.xpath("normalize-space(//h1/text())").get(),
#     FIELD_NAMES[1]: prem,
#     FIELD_NAMES[2]: respObj.xpath("normalize-space((//div[contains(@class, 'address')]/text())[2])").get(),
#     FIELD_NAMES[3]: f'''{respObj.xpath("normalize-space(//i[contains(@class, 'phone')]/parent::p/text()[last()])").get()}''',
#     FIELD_NAMES[4]: respObj.xpath("normalize-space(//ul[@class='breadcrumb']/li[3]/a/text())").get(),
#     FIELD_NAMES[5]: respObj.xpath("normalize-space(//ul[@class='breadcrumb']/li[4]/a/text())").get(),
#     FIELD_NAMES[6]: respObj.xpath("normalize-space(//ul[@class='breadcrumb']/li[5]/a/text())").get(),
#     FIELD_NAMES[7]: respObj.xpath("normalize-space(//span[contains(text(), 'Prix')]/following-sibling::span/text())").get(),
#     FIELD_NAMES[8]: f'''{respObj.xpath("normalize-space(//span[text()='Services']/parent::div/text()[2])").get()}{respObj.xpath("normalize-space((//span[text()='Services']/parent::div/span[@style]/text())[last()])").get()}''',
#     FIELD_NAMES[9]: f'''{respObj.xpath("normalize-space(//span[text()='Styles']/parent::div/text()[2])").get()}{respObj.xpath("normalize-space((//span[text()='Styles']/parent::div/span[@style]/text())[last()])").get()}''',
#     FIELD_NAMES[10]: respObj.xpath("normalize-space(//span[contains(text(), 'Formation')]/parent::div/text()[last()])").get(),
#     FIELD_NAMES[11]: respObj.xpath("normalize-space(//span[text()='Offre services']/following-sibling::p/text())").get(),
#     FIELD_NAMES[12]: respObj.xpath("normalize-space(//span[contains(text(), 'Quels sont les services inclus dans le forfait mariage')]/parent::li/div/text())").get(),
#     FIELD_NAMES[13]: respObj.xpath("normalize-space(//span[contains(text(), 'avance dois-je vous contacter')]/parent::li/div/text())").get(),
#     FIELD_NAMES[14]: ", ".join(i.strip() for i in tailleDuGroupe),
#     FIELD_NAMES[15]: respObj.xpath("normalize-space(//span[contains(text(), 'R??pertoire')]/parent::li/div/text())").get(),
#     FIELD_NAMES[16]: respObj.xpath("normalize-space(//span[contains(text(), 'Est-il possible de demander une chanson qui ne figure pas dans le r??pertoire')]/parent::li/div/text())").get(),
#     FIELD_NAMES[17]: respObj.xpath("normalize-space(//span[contains(text(), 'Exp??rience')]/parent::li/div/text())").get(),
#     FIELD_NAMES[18]: respObj.xpath("normalize-space(//span[contains(text(), 'Disposez-vous de votre propre mat??riel')]/parent::li/div/text())").get(),
#     FIELD_NAMES[19]: respObj.xpath("normalize-space(//span[contains(text(), 'Avez-vous besoin de mat??riel sp??cifique ou de conditions particuli??res pour pouvoir travailler')]/parent::li/div/text())").get(),
#     FIELD_NAMES[20]: respObj.xpath("normalize-space(//span[contains(text(), 'Pouvez-vous vous d??placer')]/parent::li/div/text())").get(),
#     FIELD_NAMES[21]: respObj.xpath("normalize-space(//span[contains(text(), 'Facturez-vous les d??placements')]/parent::li/div/text())").get(),
#     FIELD_NAMES[22]: respObj.xpath("normalize-space(//span[contains(text(), 'un mariage par jour')]/parent::li/div/text())").get(),
#     FIELD_NAMES[23]: respObj.xpath("normalize-space(//span[contains(text(), 'Travaillez-vous seul ou en ??quipe')]/parent::li/div/text())").get(),
#     FIELD_NAMES[24]: respObj.xpath("normalize-space(//span[contains(text(), 'Combien de temps dure la prestation')]/parent::li/div/text())").get(),
#     FIELD_NAMES[25]: respObj.xpath("normalize-space(//span[contains(text(), 'Combien de temps de pr??paration avez-vous besoin')]/parent::li/div/text())").get(),
#     FIELD_NAMES[26]: respObj.xpath("normalize-space(//span[contains(text(), 'Acceptez-vous de travailler en plein air')]/parent::li/div/text())").get(),
#     FIELD_NAMES[27]: respObj.xpath("normalize-space(//span[contains(text(), 'Facturez-vous par heure ou par ??v??nement')]/parent::li/div/text())").get(),
#     FIELD_NAMES[28]: respObj.xpath("normalize-space(//span[contains(text(), 'accepteriez-vous de faire des heures suppl??mentaires')]/parent::li/div/text())").get(),
#     FIELD_NAMES[29]: respObj.xpath("normalize-space(//span[contains(text(), 'Quel est le tarif des heures suppl??mentaires')]/parent::li/div/text())").get(),
#     FIELD_NAMES[30]: respObj.xpath("normalize-space(//span[contains(text(), 'effectue le paiement')]/parent::li/div/text())").get(),
#     FIELD_NAMES[31]: driver.current_url, 
# }


#=========================================================================================================================================================================


#--Organisation--#
# FIELD_NAMES = ['Name', 'Type', 'Address', 'Phone', 'Lvl 1 Category', 'Lvl 2 Category', 'Lvl 3 Category', 'Prix par menu', 'Capacit?? mariage','C??r??monies','Quels services proposez-vous', 'Organisez-vous les mariages religieux non catholiques', 'Dans quels types de c??r??monies vous sp??cialisez-vous', 'Quelle est votre m??thode de travail', 'Comment s effectue le paiement', 'Source Url']
# prem = respObj.xpath("//h1/following-sibling::i/@class").get()
# if "premium" in prem:
#     prem = "Premium"
# quelServices = respObj.xpath("//span[contains(text(), 'Quels services proposez-vous')]/parent::li/div/div/div/text()").getall()
# data = {
#     FIELD_NAMES[0]: respObj.xpath("normalize-space(//h1/text())").get(),
#     FIELD_NAMES[1]: prem,
#     FIELD_NAMES[2]: respObj.xpath("normalize-space((//div[contains(@class, 'address')]/text())[2])").get(),
#     FIELD_NAMES[3]: f'''{respObj.xpath("normalize-space(//i[contains(@class, 'phone')]/parent::p/text()[last()])").get()}''',
#     FIELD_NAMES[4]: respObj.xpath("normalize-space(//ul[@class='breadcrumb']/li[3]/a/text())").get(),
#     FIELD_NAMES[5]: respObj.xpath("normalize-space(//ul[@class='breadcrumb']/li[4]/a/text())").get(),
#     FIELD_NAMES[6]: respObj.xpath("normalize-space(//ul[@class='breadcrumb']/li[5]/a/text())").get(),
#     FIELD_NAMES[7]: respObj.xpath("normalize-space(//span[contains(text(), 'Prix')]/following-sibling::span/text())").get(),
#     FIELD_NAMES[8]: respObj.xpath("normalize-space(//span[contains(text(), 'Capacit?? mariage')]/parent::div/text()[last()])").get(),
#     FIELD_NAMES[9]: respObj.xpath("normalize-space(//span[contains(text(), 'C??r??monies')]/parent::div/text()[last()])").get(),
#     FIELD_NAMES[10]: ", ".join(i.strip() for i in quelServices),
#     FIELD_NAMES[11]: respObj.xpath("normalize-space(//span[contains(text(), 'Organisez-vous les mariages religieux non catholiques')]/parent::li/div/text())").get(),
#     FIELD_NAMES[12]: respObj.xpath("normalize-space(//span[contains(text(), 'Dans quels types de c??r??monies vous sp??cialisez-vous')]/parent::li/div/text())").get(),
#     FIELD_NAMES[13]: respObj.xpath("normalize-space(//span[contains(text(), 'Quelle est votre m??thode de travail')]/parent::li/div/text())").get(),
#     FIELD_NAMES[14]: respObj.xpath("normalize-space(//span[contains(text(), 'effectue le paiement')]/parent::li/div/text())").get(),
#     FIELD_NAMES[15]: driver.current_url, 
# }


#=========================================================================================================================================================================


#--Video--#
# FIELD_NAMES = ['Name', 'Type', 'Address', 'Phone', 'Lvl 1 Category', 'Lvl 2 Category', 'Lvl 3 Category', 'Prix par menu', 'Services', 'Formule mariage', 'Mobilit??', 'Combien de temps ?? l avance dois-je vous contacter', 'Couvrez-vous plus d un mariage par jour','Facturez-vous les d??placements','Quel style de vid??o r??alisez-vous','Quelles techniques proposez-vous','Utilisez-vous une technique particuli??re ou novatrice','Quel type de mat??riel utilisez-vous','Travaillez-vous seul ou en ??quipe','Avez-vous un rempla??ant en cas d emp??chement','Vous r??servez-vous le droit de publier les vid??os du mariage','Quel est le temps aproximatif de livraison du reportage final','Facturez-vous par heure ou par ??v??nement','Si besoin est, accepteriez-vous de faire des heures suppl??mentaires','Quel est le tarif des heures suppl??mentaires','Comment s effectue le paiement','Quelle m??thode de travail utilisez-vous','Source Url']

# quelVideo = respObj.xpath("//span[contains(text(), 'Quel style de vid??o r??alisez-vous')]/parent::li/div/div/div/text()").getall()
# quelTechnique = respObj.xpath("//span[contains(text(), 'Quelles techniques proposez-vous')]/parent::li/div/div/div/text()").getall()
# data = {
#     FIELD_NAMES[0]: respObj.xpath("normalize-space(//h1/text())").get(),
#     FIELD_NAMES[1]: respObj.xpath("//h1/following-sibling::i/@class").get(),
#     FIELD_NAMES[2]: respObj.xpath("normalize-space((//div[contains(@class, 'address')]/text())[2])").get(),
#     FIELD_NAMES[3]: f'''{respObj.xpath("normalize-space(//i[contains(@class, 'phone')]/parent::p/text()[last()])").get()}''',
#     FIELD_NAMES[4]: respObj.xpath("normalize-space(//ul[@class='breadcrumb']/li[3]/a/text())").get(),
#     FIELD_NAMES[5]: respObj.xpath("normalize-space(//ul[@class='breadcrumb']/li[4]/a/text())").get(),
#     FIELD_NAMES[6]: respObj.xpath("normalize-space(//ul[@class='breadcrumb']/li[5]/a/text())").get(),
#     FIELD_NAMES[7]: respObj.xpath("normalize-space(//span[contains(text(), 'Prix')]/following-sibling::span/text())").get(),
#     FIELD_NAMES[8]: f'''{respObj.xpath("normalize-space(//span[text()='Services']/parent::div/text()[2])").get()}{respObj.xpath("normalize-space((//span[text()='Services']/parent::div/span[@style]/text())[last()])").get()}''',
#     FIELD_NAMES[9]: f'''{respObj.xpath("normalize-space(//span[text()='Formule mariage']/parent::div/text()[2])").get()}{respObj.xpath("normalize-space((//span[text()='Formule mariage']/parent::div/span[@style]/text())[last()])").get()}''',
#     FIELD_NAMES[10]: respObj.xpath("normalize-space(//span[text()='Mobilit??']/parent::div/text()[last()])").get(),
#     FIELD_NAMES[11]: respObj.xpath("normalize-space(//span[contains(text(), 'avance dois-je vous contacter')]/parent::li/div/text())").get(),
#     FIELD_NAMES[12]: respObj.xpath("normalize-space(//span[contains(text(), 'un mariage par jour')]/parent::li/div/text())").get(),
#     FIELD_NAMES[13]: respObj.xpath("normalize-space(//span[contains(text(), 'Facturez-vous les d??placements')]/parent::li/div/text())").get(),
#     FIELD_NAMES[14]: ", ".join(i.strip() for i in quelVideo),
#     FIELD_NAMES[15]: ", ".join(i.strip() for i in quelTechnique),
#     FIELD_NAMES[16]: respObj.xpath("normalize-space(//span[contains(text(), 'Utilisez-vous une technique particuli??re ou novatrice')]/parent::li/div/text())").get(),
#     FIELD_NAMES[17]: respObj.xpath("normalize-space(//span[contains(text(), 'Quel type de mat??riel utilisez-vous')]/parent::li/div/text())").get(),
#     FIELD_NAMES[18]: respObj.xpath("normalize-space(//span[contains(text(), 'Travaillez-vous seul ou en ??quipe')]/parent::li/div/text())").get(),
#     FIELD_NAMES[19]: respObj.xpath("normalize-space(//span[contains(text(), 'Avez-vous un rempla??ant en cas')]/parent::li/div/text())").get(),
#     FIELD_NAMES[20]: respObj.xpath("normalize-space(//span[contains(text(), 'Vous r??servez-vous le droit de publier les vid??os du mariage')]/parent::li/div/text())").get(),
#     FIELD_NAMES[21]: respObj.xpath("normalize-space(//span[contains(text(), 'Quel est le temps aproximatif de livraison du reportage final')]/parent::li/div/text())").get(),
#     FIELD_NAMES[22]: respObj.xpath("normalize-space(//span[contains(text(), 'Facturez-vous par heure ou par ??v??nement')]/parent::li/div/text())").get(),
#     FIELD_NAMES[23]: respObj.xpath("normalize-space(//span[contains(text(), 'Si besoin est, accepteriez-vous de faire des heures suppl??mentaires')]/parent::li/div/text())").get(),
#     FIELD_NAMES[24]: respObj.xpath("normalize-space(//span[contains(text(), 'Quel est le tarif des heures suppl??mentaires')]/parent::li/div/text())").get(),
#     FIELD_NAMES[25]: respObj.xpath("normalize-space(//span[contains(text(), 'effectue le paiement')]/parent::li/div/text())").get(),
#     FIELD_NAMES[26]: respObj.xpath("normalize-space(//span[contains(text(), 'Quelle m??thode de travail utilisez-vous')]/parent::li/div/text())").get(),
#     FIELD_NAMES[27]: driver.current_url,      
# }


#=========================================================================================================================================================================


#--Catering--#

# FIELD_NAMES = ['Name', 'Type', 'Address', 'Phone', 'Lvl 1 Category', 'Lvl 2 Category', 'Lvl 3 Category', 'Prix par menu', 'Invites', 'Services', 'Offre services', 'Existe-t-il une commande minimum', 'Disposez-vous de salles pour la r??ception', 'Cuisinez-vous sur le lieu de la r??ception', 'Est-il possible dadapter ou de modifier les menus', 'Proposez-vous des menus personnalis??s', 'Quel type de cuisine proposez-vous', 'Proposez-vous des menus sp??cifiques', 'Proposez-vous des g??teaux de mariage', 'Y a-t-il une limite horaire ?? respecter pour l ??v??nement', 'Le photographe est-il impos??', 'Exclusivit?? musique', 'C??l??brez-vous plus dun ??v??nement par jour', 'Comment s effectue le paiement', 'Source Url']
# quelType = respObj.xpath("//span[contains(text(), 'Quel type de cuisine proposez-vous')]/parent::li/div/div/div/text()").getall()
# menuSpecs = respObj.xpath("//span[contains(text(), 'Proposez-vous des menus sp??cifiques')]/parent::li/div/div/div/text()").getall()
# data = {
#     FIELD_NAMES[0]: respObj.xpath("normalize-space(//h1/text())").get(),
#     FIELD_NAMES[1]: respObj.xpath("//h1/following-sibling::i/@class").get(),
#     FIELD_NAMES[2]: respObj.xpath("normalize-space((//div[contains(@class, 'address')]/text())[2])").get(),
#     FIELD_NAMES[3]: f'''{respObj.xpath("normalize-space(//i[contains(@class, 'phone')]/parent::p/text()[last()])").get()}''',
#     FIELD_NAMES[4]: respObj.xpath("normalize-space(//ul[@class='breadcrumb']/li[3]/a/text())").get(),
#     FIELD_NAMES[5]: respObj.xpath("normalize-space(//ul[@class='breadcrumb']/li[4]/a/text())").get(),
#     FIELD_NAMES[6]: respObj.xpath("normalize-space(//ul[@class='breadcrumb']/li[5]/a/text())").get(),
#     FIELD_NAMES[7]: respObj.xpath("normalize-space(//span[text()='Location du lieu' or contains(text(), 'menu') or contains(text(), 'Menus')]/following-sibling::span/text())").get(),
#     FIELD_NAMES[8]: respObj.xpath('''normalize-space(//span[text()="N?? d'invit??s "]/following-sibling::span/text())''').get(),
#     #FIELD_NAMES[9]: respObj.xpath("normalize-space(//span[text()='Espaces']/parent::div/text()[last()])").get(),
#     FIELD_NAMES[9]: f'''{respObj.xpath("normalize-space(//span[text()='Services']/parent::div/text()[2])").get()}{respObj.xpath("normalize-space((//span[text()='Services']/parent::div/span[@style]/text())[last()])").get()}''',
#     FIELD_NAMES[10]: respObj.xpath("normalize-space(//span[text()='Offre services']/following-sibling::p/text())").get(),
#     #FIELD_NAMES[12]: respObj.xpath("normalize-space(//span[text()='Logement']/parent::div/text()[last()])").get(),
#     FIELD_NAMES[11]: respObj.xpath("normalize-space(//span[contains(text(), 'Existe-t-il une commande minimum')]/parent::li/div/text())").get(),
#     FIELD_NAMES[12]: respObj.xpath("normalize-space(//span[contains(text(), 'Disposez-vous de salles pour la r??ception')]/parent::li/div/text())").get(),
#     FIELD_NAMES[13]: respObj.xpath("normalize-space(//span[contains(text(), 'Cuisinez-vous sur le lieu de la r??ception')]/parent::li/div/text())").get(),
#     FIELD_NAMES[14]: respObj.xpath("normalize-space(//span[contains(text(), 'adapter ou de modifier les menus')]/parent::li/div/text())").get(),
#     FIELD_NAMES[15]: respObj.xpath("normalize-space(//span[contains(text(), 'Proposez-vous des menus personnalis??s')]/parent::li/div/text())").get(),
#     FIELD_NAMES[16]: ", ".join(i.strip() for i in quelType),
#     FIELD_NAMES[17]: ", ".join(i.strip() for i in menuSpecs),
#     FIELD_NAMES[18]: respObj.xpath("normalize-space(//span[contains(text(), 'Proposez-vous des g??teaux de mariage')]/parent::li/div/text())").get(),
#     FIELD_NAMES[19]: respObj.xpath("normalize-space(//span[contains(text(), 'limite horaire ?? respecter pour')]/parent::li/div/text())").get(),
#     FIELD_NAMES[20]: respObj.xpath("normalize-space(//span[contains(text(), 'Le photographe est-il impos??')]/parent::li/div/text())").get(),
#     FIELD_NAMES[21]: respObj.xpath("normalize-space(//span[contains(text(), 'Exclusivit?? musique')]/parent::li/div/text())").get(),
#     FIELD_NAMES[22]: respObj.xpath("normalize-space(//span[contains(text(), 'C??l??brez-vous plus')]/parent::li/div/text())").get(),
#     FIELD_NAMES[23]: respObj.xpath("normalize-space(//span[contains(text(), 'effectue le paiement')]/parent::li/div/text())").get(),
#     FIELD_NAMES[24]: driver.current_url,
# }