# Scrapy settings for steamCommunityMarket project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Googlebot'

SPIDER_MODULES = ['steamCommunityMarket.spiders']
NEWSPIDER_MODULE = 'steamCommunityMarket.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

DOWNLOADER_MIDDLEWARES = {
    'scrapy_selenium.SeleniumMiddleware': 800,
}

SELENIUM_DRIVER_NAME = 'chrome'

# ----   SETTINGS FOR LINUX   ---

# SELENIUM_DRIVER_EXECUTABLE_PATH = "../chromedriver"
# SELENIUM_DRIVER_ARGUMENTS=['--headless', '--no-sandbox']


# ---   SETTINGS FOR WINDOWS   ---

SELENIUM_DRIVER_ARGUMENTS=[]
SELENIUM_DRIVER_EXECUTABLE_PATH = "../chromedriver84"
# SELENIUM_DRIVER_ARGUMENTS=['--headless']

FEED_EXPORT_ENCODING = 'utf-8'
