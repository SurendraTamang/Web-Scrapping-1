from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium_stealth import stealth
from scrapy import Selector
import time
import json
import os


#-- Initializing the chrome driver --#
def initChromeDriver():
    chrome_options = webdriver.ChromeOptions()
    # prefs = {"download.default_directory" : "/some/path"}
    # chromeOptions.add_experimental_option("prefs",prefs)
    chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--incognito')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(os.environ.get('chromedriver'), chrome_options=chrome_options) 
    # driver = webdriver.Chrome('./chromedriver',chrome_options=chrome_options)
    
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    return driver

driver = initChromeDriver()
driver.maximize_window()

driver.get("https://web.bcpa.net/bcpaclient/#/Record-Search")

WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@id='txtField']")))
time.sleep(1)

driver.find_element_by_xpath("//input[@id='txtField']").clear()
search_box = driver.find_element_by_xpath("//input[@id='txtField']")
#-- Change the address in the below line --#
search_box.send_keys("458 LAKESIDE CIR SUNRISE, 33326")
search_box.send_keys(Keys.ENTER)

WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[text()='Property Summary']")))

html = driver.page_source
respObj = Selector(text=html)

propertySummary = {
    'Property Id': respObj.xpath("normalize-space(//div[@id='folioNumberId']/span/a/text())").get(),
    'Physical Address': respObj.xpath("normalize-space(//div[@id='situsAddressId']/span/a/text())").get(),
    'Neighborhood': respObj.xpath("normalize-space(//div[@id='neighborhood']/text())").get(),
    'Property Use': respObj.xpath("normalize-space(//div[@id='useCodeId']/text())").get(),
    'Adj. Bldg. S.F.': respObj.xpath("normalize-space(//span[@id='bldgSqFTId']/text())").get(),
    'Bldg Under Air S.F': respObj.xpath("normalize-space(//div[@id='bldgUnderAirFootageId']/text())").get(),
    'Effective Year': respObj.xpath("normalize-space(//div[@id='effectiveAgeId']/text())").get(),
    'Year Built': respObj.xpath("normalize-space(//div[@id='actualAgeId']/text())").get(),
    'Units/Beds/Baths': respObj.xpath("normalize-space(//div[@id='unitsBedsBathsId']/text())").get(),
    'Abbr. Legal Des': respObj.xpath("normalize-space(//div[@id='legalDescId']/text())").get()
}

propAssmtLi = []
paTableRows = respObj.xpath("//div[@id='currentTaxYearId']/parent::td/parent::tr/parent::tbody/tr")
for tabRow in paTableRows:
    if tabRow.xpath("normalize-space(.//td[1]/div/text())").get():
        propAssmtLi.append(
            {
                'Year': tabRow.xpath("normalize-space(.//td[1]/div/text())").get(),
                'Assessed / SOH Value': tabRow.xpath("normalize-space(.//td[6]/div/text())").get(),
                'Tax': tabRow.xpath("normalize-space(.//td[7]/div/text())").get(),
            }
        )

saleHistLi = []
shTableRows = respObj.xpath("//div[@id='salesHistoryDate1']/parent::td/parent::tr/parent::tbody/tr")
for tabRow in shTableRows:
    if tabRow.xpath("normalize-space(.//td[1]/div/text())").get():
        saleHistLi.append(
            {
                'Date': tabRow.xpath("normalize-space(.//td[1]/div/text())").get(),
                'Type': tabRow.xpath("normalize-space(.//td[2]/div/text())").get(),
                'Qualified/Disqualified': tabRow.xpath("normalize-space(.//td[3]/div/text())").get(),
                'Price': tabRow.xpath("normalize-space(.//td[4]/div/text())").get(),
            }
        )

recSaleLi = []
rsTableRows = respObj.xpath("//div[@id='recentSaleFolioNumber1']/parent::td/parent::tr/parent::tbody/tr")
for tabRow in rsTableRows:
    if tabRow.xpath("normalize-space(.//td[1]/div/text())").get():
        recSaleLi.append(
            {
                'Date': tabRow.xpath("normalize-space(.//td[2]/div/text())").get(),
                'Type': tabRow.xpath("normalize-space(.//td[3]/div/text())").get(),
                'Qualified/Disqualified': tabRow.xpath("normalize-space(.//td[4]/div/text())").get(),
                'Price': tabRow.xpath("normalize-space(.//td[5]/div/text())").get(),
                'Book/Page Or CIN': tabRow.xpath("normalize-space(.//td[6]/div/text())").get(),
                'Property Address': tabRow.xpath("normalize-space(.//td[7]/div/text())").get(),
            }
        )

dataDict = {
    'Property Summary': propertySummary,
    'Property Assessment': propAssmtLi,
    'Sales History': saleHistLi,
    'Recent Sales': recSaleLi,
}

#-- Writing a dictionary to a JSON file --#
json_object = json.dumps(dataDict, indent = 4)
with open("sample1.json", "w") as outfile:
    outfile.write(json_object)


driver.quit()