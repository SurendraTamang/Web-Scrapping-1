# -*- coding: utf-8 -*-

SPIDER_MODULES = ['avalonCommunities.spiders']
NEWSPIDER_MODULE = 'avalonCommunities.spiders'

BOT_NAME = 'Googlebot'
# USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36 Edg/86.0.622.51'
ROBOTSTXT_OBEY = False
DOWNLOAD_DELAY = 2
AUTOTHROTTLE_ENABLED = True

FEED_EXPORT_ENCODING = 'utf-8'

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400
}

# LOG_FILE = 'avalonLogs.txt'
# LOG_ENCODING = 'utf-8'
# LOG_LEVEL = 'ERROR'