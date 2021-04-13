from selenium import webdriver
from selenium_stealth import stealth
import time
import pandas as pd


#-- Writing Data to a HTML file --#
def writeHTML(data, file_name):
    f = open(file_name, "w", encoding="utf-8")
    f.write(data)
    f.close()

#-- Generate output file name --#
def genFilename(url):
    f1 = url.replace("https://www.","")
    f2 = f1.replace("http://www.","")
    f3 = f2.replace("/","_")
    f4 = f3.replace(".","_")
    f5 = f4.replace("?","_")
    f6 = f5.replace("=","_")
    f7 = f6.replace("&","_")
    return f'''./outputFiles/{f7}.html'''

#-- Initializing the chrome driver --#
def initChromeDriver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    #-- Uncomment the below two lines while running on MAC/LINUX  --#
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--incognito')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    # driver = webdriver.Chrome(os.environ.get('chromedriver'), chrome_options=chrome_options) 
    driver = webdriver.Chrome('./chromedriver',chrome_options=chrome_options)
    
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    return driver


if __name__ == "__main__":
    df = pd.read_excel("input.xlsx")
    for _,val in df.iterrows():
        statUrl = val['static url']
        queryLi = val['query list'].split(",")
        for query in queryLi:
            url = f"{statUrl}{query}"
            driver = initChromeDriver()
            driver.maximize_window()
            driver.get(url)

            html = driver.page_source
            time.sleep(3)

            writeHTML(html, genFilename(url))

    driver.quit()

    