from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from scrapy import Selector
from selenium_stealth import stealth
import os
import csv
import time


FILE_NAME = '/content/drive/MyDrive/fiverrWorkspace/marriagesData/music/MusicFrance.csv'
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

driver.get("https://www.mariages.net/musique-mariage")
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
    'Prix par menu',
    'Services',
    'Styles',
    'Formation',
    'Offre services',
    'Quels sont les services inclus dans le forfait mariage',
    'Combien de temps à l avance dois-je vous contacter',
    'Taille du groupe',
    'Répertoire',
    'Est-il possible de demander une chanson qui ne figure pas dans le répertoire',
    'Expérience',
    'Disposez-vous de votre propre matériel',
    'Avez-vous besoin de matériel spécifique ou de conditions particulières pour pouvoir travailler',
    'Pouvez-vous vous déplacer',
    'Facturez-vous les déplacements',
    'Couvrez-vous plus d un mariage par jour',
    'Travaillez-vous seul ou en équipe',
    'Combien de temps dure la prestation',
    'Combien de temps de préparation avez-vous besoin',
    'Acceptez-vous de travailler en plein air',
    'Facturez-vous par heure ou par événement',
    'accepteriez-vous de faire des heures supplémentaires',
    'Quel est le tarif des heures supplémentaires',
    'Comment s effectue le paiement',
    'Base Url'
  ]
  prem = respObj.xpath("//h1/following-sibling::i/@class").get()
  try:
    if "premium" in prem:
        prem = "Premium"
  except:
    pass
  tailleDuGroupe = respObj.xpath("//span[contains(text(), 'Taille du groupe')]/parent::li/div/div/div/text()").getall()
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
      FIELD_NAMES[9]: f'''{respObj.xpath("normalize-space(//span[text()='Styles']/parent::div/text()[2])").get()}{respObj.xpath("normalize-space((//span[text()='Styles']/parent::div/span[@style]/text())[last()])").get()}''',
      FIELD_NAMES[10]: respObj.xpath("normalize-space(//span[contains(text(), 'Formation')]/parent::div/text()[last()])").get(),
      FIELD_NAMES[11]: respObj.xpath("normalize-space(//span[text()='Offre services']/following-sibling::p/text())").get(),
      FIELD_NAMES[12]: respObj.xpath("normalize-space(//span[contains(text(), 'Quels sont les services inclus dans le forfait mariage')]/parent::li/div/text())").get(),
      FIELD_NAMES[13]: respObj.xpath("normalize-space(//span[contains(text(), 'avance dois-je vous contacter')]/parent::li/div/text())").get(),
      FIELD_NAMES[14]: ", ".join(i.strip() for i in tailleDuGroupe),
      FIELD_NAMES[15]: respObj.xpath("normalize-space(//span[contains(text(), 'Répertoire')]/parent::li/div/text())").get(),
      FIELD_NAMES[16]: respObj.xpath("normalize-space(//span[contains(text(), 'Est-il possible de demander une chanson qui ne figure pas dans le répertoire')]/parent::li/div/text())").get(),
      FIELD_NAMES[17]: respObj.xpath("normalize-space(//span[contains(text(), 'Expérience')]/parent::li/div/text())").get(),
      FIELD_NAMES[18]: respObj.xpath("normalize-space(//span[contains(text(), 'Disposez-vous de votre propre matériel')]/parent::li/div/text())").get(),
      FIELD_NAMES[19]: respObj.xpath("normalize-space(//span[contains(text(), 'Avez-vous besoin de matériel spécifique ou de conditions particulières pour pouvoir travailler')]/parent::li/div/text())").get(),
      FIELD_NAMES[20]: respObj.xpath("normalize-space(//span[contains(text(), 'Pouvez-vous vous déplacer')]/parent::li/div/text())").get(),
      FIELD_NAMES[21]: respObj.xpath("normalize-space(//span[contains(text(), 'Facturez-vous les déplacements')]/parent::li/div/text())").get(),
      FIELD_NAMES[22]: respObj.xpath("normalize-space(//span[contains(text(), 'un mariage par jour')]/parent::li/div/text())").get(),
      FIELD_NAMES[23]: respObj.xpath("normalize-space(//span[contains(text(), 'Travaillez-vous seul ou en équipe')]/parent::li/div/text())").get(),
      FIELD_NAMES[24]: respObj.xpath("normalize-space(//span[contains(text(), 'Combien de temps dure la prestation')]/parent::li/div/text())").get(),
      FIELD_NAMES[25]: respObj.xpath("normalize-space(//span[contains(text(), 'Combien de temps de préparation avez-vous besoin')]/parent::li/div/text())").get(),
      FIELD_NAMES[26]: respObj.xpath("normalize-space(//span[contains(text(), 'Acceptez-vous de travailler en plein air')]/parent::li/div/text())").get(),
      FIELD_NAMES[27]: respObj.xpath("normalize-space(//span[contains(text(), 'Facturez-vous par heure ou par événement')]/parent::li/div/text())").get(),
      FIELD_NAMES[28]: respObj.xpath("normalize-space(//span[contains(text(), 'accepteriez-vous de faire des heures supplémentaires')]/parent::li/div/text())").get(),
      FIELD_NAMES[29]: respObj.xpath("normalize-space(//span[contains(text(), 'Quel est le tarif des heures supplémentaires')]/parent::li/div/text())").get(),
      FIELD_NAMES[30]: respObj.xpath("normalize-space(//span[contains(text(), 'effectue le paiement')]/parent::li/div/text())").get(),
      FIELD_NAMES[31]: driver.current_url, 
  }
  # print(data)
  writeCSV(data, FIELD_NAMES, FILE_NAME)
  data.clear()




#--Organisation--#
# FIELD_NAMES = ['Name', 'Type', 'Address', 'Phone', 'Lvl 1 Category', 'Lvl 2 Category', 'Lvl 3 Category', 'Prix par menu', 'Capacité mariage','Cérémonies','Quels services proposez-vous', 'Organisez-vous les mariages religieux non catholiques', 'Dans quels types de cérémonies vous spécialisez-vous', 'Quelle est votre méthode de travail', 'Comment s effectue le paiement', 'Source Url']
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
#     FIELD_NAMES[8]: respObj.xpath("normalize-space(//span[contains(text(), 'Capacité mariage')]/parent::div/text()[last()])").get(),
#     FIELD_NAMES[9]: respObj.xpath("normalize-space(//span[contains(text(), 'Cérémonies')]/parent::div/text()[last()])").get(),
#     FIELD_NAMES[10]: ", ".join(i.strip() for i in quelServices),
#     FIELD_NAMES[11]: respObj.xpath("normalize-space(//span[contains(text(), 'Organisez-vous les mariages religieux non catholiques')]/parent::li/div/text())").get(),
#     FIELD_NAMES[12]: respObj.xpath("normalize-space(//span[contains(text(), 'Dans quels types de cérémonies vous spécialisez-vous')]/parent::li/div/text())").get(),
#     FIELD_NAMES[13]: respObj.xpath("normalize-space(//span[contains(text(), 'Quelle est votre méthode de travail')]/parent::li/div/text())").get(),
#     FIELD_NAMES[14]: respObj.xpath("normalize-space(//span[contains(text(), 'effectue le paiement')]/parent::li/div/text())").get(),
#     FIELD_NAMES[15]: driver.current_url, 
# }



#--Video--#
# FIELD_NAMES = ['Name', 'Type', 'Address', 'Phone', 'Lvl 1 Category', 'Lvl 2 Category', 'Lvl 3 Category', 'Prix par menu', 'Services', 'Formule mariage', 'Mobilité', 'Combien de temps à l avance dois-je vous contacter', 'Couvrez-vous plus d un mariage par jour','Facturez-vous les déplacements','Quel style de vidéo réalisez-vous','Quelles techniques proposez-vous','Utilisez-vous une technique particulière ou novatrice','Quel type de matériel utilisez-vous','Travaillez-vous seul ou en équipe','Avez-vous un remplaçant en cas d empêchement','Vous réservez-vous le droit de publier les vidéos du mariage','Quel est le temps aproximatif de livraison du reportage final','Facturez-vous par heure ou par événement','Si besoin est, accepteriez-vous de faire des heures supplémentaires','Quel est le tarif des heures supplémentaires','Comment s effectue le paiement','Quelle méthode de travail utilisez-vous','Source Url']

# quelVideo = respObj.xpath("//span[contains(text(), 'Quel style de vidéo réalisez-vous')]/parent::li/div/div/div/text()").getall()
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
#     FIELD_NAMES[10]: respObj.xpath("normalize-space(//span[text()='Mobilité']/parent::div/text()[last()])").get(),
#     FIELD_NAMES[11]: respObj.xpath("normalize-space(//span[contains(text(), 'avance dois-je vous contacter')]/parent::li/div/text())").get(),
#     FIELD_NAMES[12]: respObj.xpath("normalize-space(//span[contains(text(), 'un mariage par jour')]/parent::li/div/text())").get(),
#     FIELD_NAMES[13]: respObj.xpath("normalize-space(//span[contains(text(), 'Facturez-vous les déplacements')]/parent::li/div/text())").get(),
#     FIELD_NAMES[14]: ", ".join(i.strip() for i in quelVideo),
#     FIELD_NAMES[15]: ", ".join(i.strip() for i in quelTechnique),
#     FIELD_NAMES[16]: respObj.xpath("normalize-space(//span[contains(text(), 'Utilisez-vous une technique particulière ou novatrice')]/parent::li/div/text())").get(),
#     FIELD_NAMES[17]: respObj.xpath("normalize-space(//span[contains(text(), 'Quel type de matériel utilisez-vous')]/parent::li/div/text())").get(),
#     FIELD_NAMES[18]: respObj.xpath("normalize-space(//span[contains(text(), 'Travaillez-vous seul ou en équipe')]/parent::li/div/text())").get(),
#     FIELD_NAMES[19]: respObj.xpath("normalize-space(//span[contains(text(), 'Avez-vous un remplaçant en cas')]/parent::li/div/text())").get(),
#     FIELD_NAMES[20]: respObj.xpath("normalize-space(//span[contains(text(), 'Vous réservez-vous le droit de publier les vidéos du mariage')]/parent::li/div/text())").get(),
#     FIELD_NAMES[21]: respObj.xpath("normalize-space(//span[contains(text(), 'Quel est le temps aproximatif de livraison du reportage final')]/parent::li/div/text())").get(),
#     FIELD_NAMES[22]: respObj.xpath("normalize-space(//span[contains(text(), 'Facturez-vous par heure ou par événement')]/parent::li/div/text())").get(),
#     FIELD_NAMES[23]: respObj.xpath("normalize-space(//span[contains(text(), 'Si besoin est, accepteriez-vous de faire des heures supplémentaires')]/parent::li/div/text())").get(),
#     FIELD_NAMES[24]: respObj.xpath("normalize-space(//span[contains(text(), 'Quel est le tarif des heures supplémentaires')]/parent::li/div/text())").get(),
#     FIELD_NAMES[25]: respObj.xpath("normalize-space(//span[contains(text(), 'effectue le paiement')]/parent::li/div/text())").get(),
#     FIELD_NAMES[26]: respObj.xpath("normalize-space(//span[contains(text(), 'Quelle méthode de travail utilisez-vous')]/parent::li/div/text())").get(),
#     FIELD_NAMES[27]: driver.current_url,      
# }



#--Catering--#

# FIELD_NAMES = ['Name', 'Type', 'Address', 'Phone', 'Lvl 1 Category', 'Lvl 2 Category', 'Lvl 3 Category', 'Prix par menu', 'Invites', 'Services', 'Offre services', 'Existe-t-il une commande minimum', 'Disposez-vous de salles pour la réception', 'Cuisinez-vous sur le lieu de la réception', 'Est-il possible dadapter ou de modifier les menus', 'Proposez-vous des menus personnalisés', 'Quel type de cuisine proposez-vous', 'Proposez-vous des menus spécifiques', 'Proposez-vous des gâteaux de mariage', 'Y a-t-il une limite horaire à respecter pour l événement', 'Le photographe est-il imposé', 'Exclusivité musique', 'Célébrez-vous plus dun événement par jour', 'Comment s effectue le paiement', 'Source Url']
# quelType = respObj.xpath("//span[contains(text(), 'Quel type de cuisine proposez-vous')]/parent::li/div/div/div/text()").getall()
# menuSpecs = respObj.xpath("//span[contains(text(), 'Proposez-vous des menus spécifiques')]/parent::li/div/div/div/text()").getall()
# data = {
#     FIELD_NAMES[0]: respObj.xpath("normalize-space(//h1/text())").get(),
#     FIELD_NAMES[1]: respObj.xpath("//h1/following-sibling::i/@class").get(),
#     FIELD_NAMES[2]: respObj.xpath("normalize-space((//div[contains(@class, 'address')]/text())[2])").get(),
#     FIELD_NAMES[3]: f'''{respObj.xpath("normalize-space(//i[contains(@class, 'phone')]/parent::p/text()[last()])").get()}''',
#     FIELD_NAMES[4]: respObj.xpath("normalize-space(//ul[@class='breadcrumb']/li[3]/a/text())").get(),
#     FIELD_NAMES[5]: respObj.xpath("normalize-space(//ul[@class='breadcrumb']/li[4]/a/text())").get(),
#     FIELD_NAMES[6]: respObj.xpath("normalize-space(//ul[@class='breadcrumb']/li[5]/a/text())").get(),
#     FIELD_NAMES[7]: respObj.xpath("normalize-space(//span[text()='Location du lieu' or contains(text(), 'menu') or contains(text(), 'Menus')]/following-sibling::span/text())").get(),
#     FIELD_NAMES[8]: respObj.xpath('''normalize-space(//span[text()="Nº d'invités "]/following-sibling::span/text())''').get(),
#     #FIELD_NAMES[9]: respObj.xpath("normalize-space(//span[text()='Espaces']/parent::div/text()[last()])").get(),
#     FIELD_NAMES[9]: f'''{respObj.xpath("normalize-space(//span[text()='Services']/parent::div/text()[2])").get()}{respObj.xpath("normalize-space((//span[text()='Services']/parent::div/span[@style]/text())[last()])").get()}''',
#     FIELD_NAMES[10]: respObj.xpath("normalize-space(//span[text()='Offre services']/following-sibling::p/text())").get(),
#     #FIELD_NAMES[12]: respObj.xpath("normalize-space(//span[text()='Logement']/parent::div/text()[last()])").get(),
#     FIELD_NAMES[11]: respObj.xpath("normalize-space(//span[contains(text(), 'Existe-t-il une commande minimum')]/parent::li/div/text())").get(),
#     FIELD_NAMES[12]: respObj.xpath("normalize-space(//span[contains(text(), 'Disposez-vous de salles pour la réception')]/parent::li/div/text())").get(),
#     FIELD_NAMES[13]: respObj.xpath("normalize-space(//span[contains(text(), 'Cuisinez-vous sur le lieu de la réception')]/parent::li/div/text())").get(),
#     FIELD_NAMES[14]: respObj.xpath("normalize-space(//span[contains(text(), 'adapter ou de modifier les menus')]/parent::li/div/text())").get(),
#     FIELD_NAMES[15]: respObj.xpath("normalize-space(//span[contains(text(), 'Proposez-vous des menus personnalisés')]/parent::li/div/text())").get(),
#     FIELD_NAMES[16]: ", ".join(i.strip() for i in quelType),
#     FIELD_NAMES[17]: ", ".join(i.strip() for i in menuSpecs),
#     FIELD_NAMES[18]: respObj.xpath("normalize-space(//span[contains(text(), 'Proposez-vous des gâteaux de mariage')]/parent::li/div/text())").get(),
#     FIELD_NAMES[19]: respObj.xpath("normalize-space(//span[contains(text(), 'limite horaire à respecter pour')]/parent::li/div/text())").get(),
#     FIELD_NAMES[20]: respObj.xpath("normalize-space(//span[contains(text(), 'Le photographe est-il imposé')]/parent::li/div/text())").get(),
#     FIELD_NAMES[21]: respObj.xpath("normalize-space(//span[contains(text(), 'Exclusivité musique')]/parent::li/div/text())").get(),
#     FIELD_NAMES[22]: respObj.xpath("normalize-space(//span[contains(text(), 'Célébrez-vous plus')]/parent::li/div/text())").get(),
#     FIELD_NAMES[23]: respObj.xpath("normalize-space(//span[contains(text(), 'effectue le paiement')]/parent::li/div/text())").get(),
#     FIELD_NAMES[24]: driver.current_url,
# }