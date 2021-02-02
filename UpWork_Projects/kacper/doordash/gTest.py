from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from selenium_stealth import stealth


#CHROMEDRIVERPATH = os.environ.get("chromedriver")
CHROMEDRIVERPATH = "../chromedriver"

options = Options()
options.headless = True
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(CHROMEDRIVERPATH, chrome_options=options)
#driver.maximize_window()
#driver.set_window_size(1920, 1080)
stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

driver.get(f"https://www.google.com/search?q={val['gSearchQuery']}")
time.sleep(1)
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='g']")))

html = driver.page_source
f = open("./page1.html", "w")
f.write(html)
f.close()

driver.quit()