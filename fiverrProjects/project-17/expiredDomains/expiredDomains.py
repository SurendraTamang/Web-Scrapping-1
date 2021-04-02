from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from scrapy import Selector
import time
import getpass


#-- User Inputs --#
print("####################  USER LOGIN  ####################")
uname = input("Type your username: ")
pswd = getpass.getpass(prompt="Enter Password: ")

print("\n\n####################  SET FILTERS  ####################")
keyword = input("Enter Keyword: ")
wmin = input("Enter WBY Minimum Value: ")
wmax = input("Enter WBY Maximum Value: ")
amin = input("Enter ABY Minimum Value: ")
amax = input("Enter ABY Maximum Value: ")
tld = input("Enter Name in selected TLD is available: ")
print("\n\n####################  FILE NAME  ####################")
fileName = input("Enter the output file name(eg: example.txt): ")
print("\n\nLogging in....")



chrome_options = webdriver.ChromeOptions()
# prefs = {"download.default_directory" : "/some/path"}
# chromeOptions.add_experimental_option("prefs",prefs)
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--incognito')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
# driver = webdriver.Chrome(os.environ.get('chromedriver'),chrome_options=chrome_options)
driver = webdriver.Chrome('./chromedriver',chrome_options=chrome_options)
driver.maximize_window()

stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

driver.get("https://www.expireddomains.net/login/")
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[contains(@id, 'Login')]")))
time.sleep(1)

#-- User Login --#
username = driver.find_element_by_xpath("//input[contains(@id, 'Login')]")
# username.send_keys(input("Enter your username: "))
username.send_keys(uname)
password = driver.find_element_by_xpath("//input[contains(@id, 'Password')]")
# password.send_keys(input("Enter your password: "))
password.send_keys(pswd)
loginBtnElem = driver.find_element_by_xpath("//button[text()='Login']")
driver.execute_script("arguments[0].click()", loginBtnElem)

#-- Navigating to the Deleted Domains Section --#
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//a[contains(text(), 'Deleted Domains')]")))
time.sleep(1)
delDomBtnElem = driver.find_element_by_xpath("//li[@class='navbutton']/a[contains(text(), 'Deleted Domains')]")
driver.execute_script("arguments[0].click()", delDomBtnElem)

print("\nApplying Filters....")

#-- Wait till the page is loaded and then apply the filters --#
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//a[contains(text(), 'Show Filter')]")))
filterBtnElem = driver.find_element_by_xpath("//a[contains(text(), 'Show Filter')]")
driver.execute_script("arguments[0].click()", filterBtnElem)

#-- Filter1 - Search by keyword --#
try:
    containsElem = driver.find_element_by_xpath("//h3[text()='Domain Name Allowlist']/parent::div/parent::div//label[text()='contains']/following-sibling::div/input")
    containsElem.send_keys(keyword)
except:
    pass

#-- Filter2 - Search by keyword --#
try:
    wbyMin = Select(driver.find_element_by_xpath("//label[text()='WBY']/following-sibling::div[1]/select"))
    wbyMin.select_by_value(wmin)
except:
    pass
try:
    wbyMax = Select(driver.find_element_by_xpath("//label[text()='WBY']/following-sibling::div[2]/select"))
    wbyMax.select_by_value(wmax)
except:
    pass
try:
    abyMin = Select(driver.find_element_by_xpath("//label[text()='ABY']/following-sibling::div[1]/select"))
    abyMin.select_by_value(amin)
except:
    pass
try:
    abyMax = Select(driver.find_element_by_xpath("//label[text()='ABY']/following-sibling::div[2]/select"))
    abyMax.select_by_value(amax)
except:
    pass

#-- Filter3 - Search by Name in selected TLD is available --#
addTabElem = driver.find_element_by_xpath("//a[text()='Additional']")
driver.execute_script("arguments[0].click()", addTabElem)
try:
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//h3[text()='Name in selected TLD is available']")))
    tldAvlbElem = driver.find_element_by_xpath(f'''//h3[text()='Name in selected TLD is available']/parent::div/parent::div//div[contains(@class, 'checkbox')]/label/span[text()='{tld}']/preceding-sibling::input''').click()
except:
    pass

filterBtnElem = driver.find_element_by_xpath("//input[@value='Apply Filter']")
driver.execute_script("arguments[0].click()", filterBtnElem)

print("\nScraping Data in progress....")
time.sleep(4)
while True:
    time.sleep(3)

    html = driver.page_source
    respObj = Selector(text=html)

    urls = respObj.xpath("//tbody/tr/td[1]/a/@title").getall()
    urlLi = [f"{i}\n" for i in urls]

    #-- Writing the websites to the text file --#
    txtFile = open(fileName,"a")
    txtFile.writelines(urlLi)
    txtFile.close() 

    #-- Handling the Pagination --#
    nextPage = respObj.xpath("//a[contains(text(), 'Next Page')]")
    if nextPage:
        nextPageBtnElem = driver.find_element_by_xpath("//a[contains(text(), 'Next Page')]")
        driver.execute_script("arguments[0].click()", nextPageBtnElem)
    else:
        break

print("\nScraping is Complete!")
driver.quit()

