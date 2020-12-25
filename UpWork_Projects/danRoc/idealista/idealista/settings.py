# Scrapy settings for idealista project

SPIDER_MODULES = ['idealista.spiders']
NEWSPIDER_MODULE = 'idealista.spiders'

BOT_NAME = 'Googlebot'

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36 Edg/86.0.622.51'

ROBOTSTXT_OBEY = False

DOWNLOAD_DELAY = 2

# AUTOTHROTTLE_ENABLED = True

# ROTATING_PROXY_LIST_PATH = '../openProxy.txt'

# DOWNLOADER_MIDDLEWARES = {
#     'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
#     'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
# }

# SELENIUM_DRIVER_NAME = 'chrome'

# ----   SETTINGS FOR LINUX   ---

# SELENIUM_DRIVER_EXECUTABLE_PATH = "../chromedriver"
# SELENIUM_DRIVER_ARGUMENTS=['--headless', '--no-sandbox']


# ---   SETTINGS FOR WINDOWS   ---

# SELENIUM_DRIVER_ARGUMENTS=[]
# SELENIUM_DRIVER_EXECUTABLE_PATH = "../chromedriver_windows"
# SELENIUM_DRIVER_ARGUMENTS=['--headless']

FEED_EXPORT_ENCODING = 'utf-8'

# DOWNLOADER_MIDDLEWARES = {
#     'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
#     'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
#     # ...
#     # 'scrapy_proxy_pool.middlewares.ProxyPoolMiddleware': 400,
#     # 'scrapy_proxy_pool.middlewares.BanDetectionMiddleware': 401
#     # ...
# }