# -*- coding: utf-8 -*-

BOT_NAME = 'Googlebot'

SPIDER_MODULES = ['essexapartmenthomes.spiders']
NEWSPIDER_MODULE = 'essexapartmenthomes.spiders'

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36 Edg/86.0.622.51'

ROBOTSTXT_OBEY = False

DOWNLOADER_MIDDLEWARES = {
    'scrapy_selenium.SeleniumMiddleware': 800,
}

SELENIUM_DRIVER_NAME = 'chrome'

# ----   SETTINGS FOR LINUX   ---

SELENIUM_DRIVER_EXECUTABLE_PATH = "../chromedriver"
SELENIUM_DRIVER_ARGUMENTS=['--headless', '--no-sandbox']


# ---   SETTINGS FOR WINDOWS   ---

# SELENIUM_DRIVER_ARGUMENTS=[]
# SELENIUM_DRIVER_EXECUTABLE_PATH = "../chromedriver_windows"
# SELENIUM_DRIVER_ARGUMENTS=['--headless']

FEED_EXPORT_ENCODING = 'utf-8'