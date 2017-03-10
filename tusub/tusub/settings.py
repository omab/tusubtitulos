# -*- coding: utf-8 -*-

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BOT_NAME = 'tusub'

SPIDER_MODULES = ['tusub.spiders']
NEWSPIDER_MODULE = 'tusub.spiders'

# DOWNLOAD_DELAY = 1.0

USER_AGENT = 'User-Agent=Mozilla/5.0 (Windows NT 10.0; WOW64) ' + \
             'AppleWebKit/537.36 (KHTML, like Gecko) ' + \
             'Chrome/46.0.2490.86 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# tusubtitulo.com dies if we hit it too often
DOWNLOAD_DELAY = 3

COOKIES_ENABLED = True

ITEM_PIPELINES = {
    'tusub.pipelines.DownloadSubtitlePipeline': 300
}

# HTTPCACHE_ENABLED = False
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

FILES_STORE = os.path.join(BASE_DIR, 'files')
FILES_EXPIRES = 0
