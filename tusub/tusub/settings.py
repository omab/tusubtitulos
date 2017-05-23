# -*- coding: utf-8 -*-

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BOT_NAME = 'tusub'

DEBUG = False

# LOG_LEVEL = 'INFO'

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
    'tusub.pipelines.DownloadSubtitlePipeline': 300,
    'tusub.pipelines.AllocateSubtitlePipeline': 500
}

# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

FILES_STORE = os.path.join(BASE_DIR, 'files')
FILES_EXPIRES = 0

SUBTITLES_CACHE_FILE = os.path.join(BASE_DIR, 'subtitles.json')
SUBTITLES_FINAL_LOCATION = '/media/series'
SUPPORTED_VIDEO_EXTENSIONS = ['mkv', 'mp4']


SERIES = {
    '12_monkeys': {
        'enabled': True,
        'url': 'https://www.tusubtitulo.com/show/2320',
        'location': os.path.join(SUBTITLES_FINAL_LOCATION, '12_monkeys')
    },
    'arrow': {
        'enabled': True,
        'url': 'https://www.tusubtitulo.com/show/1493',
        'location': os.path.join(SUBTITLES_FINAL_LOCATION, 'arrow')
    },
    'the_big_bang_theory': {
        'enabled': True,
        'url': 'https://www.tusubtitulo.com/show/26',
        'location': os.path.join(SUBTITLES_FINAL_LOCATION, 'the_big_bang_theory')
    },
    'the_blacklist': {
        'enabled': False,
        'url': 'https://www.tusubtitulo.com/show/1832',
        'location': os.path.join(SUBTITLES_FINAL_LOCATION, 'the_blacklist')
    },
    'blindspot': {
        'enabled': False,
        'url': 'https://www.tusubtitulo.com/show/2515',
        'location': os.path.join(SUBTITLES_FINAL_LOCATION, 'blindspot')
    },
    'continuum': {
        'enabled': False,
        'url': 'https://www.tusubtitulo.com/show/1336',
        'location': os.path.join(SUBTITLES_FINAL_LOCATION, 'continuum')
    },
    'dc\'s_legends_of_tomorrow': {
        'enabled': True,
        'url': 'https://www.tusubtitulo.com/show/2651',
        'location': os.path.join(SUBTITLES_FINAL_LOCATION, 'dc\'s_legends_of_tomorrow')
    },
    'dr_who': {
        'enabled': True,
        'url': 'https://www.tusubtitulo.com/show/117',
        'location': os.path.join(SUBTITLES_FINAL_LOCATION, 'doctor_who_2005')
    },
    'falling_skies': {
        'enabled': False,
        'url': 'https://www.tusubtitulo.com/show/967',
        'location': os.path.join(SUBTITLES_FINAL_LOCATION, 'falling_skies')
    },
    'the_flash': {
        'enabled': True,
        'url': 'https://www.tusubtitulo.com/show/2125',
        'location': os.path.join(SUBTITLES_FINAL_LOCATION, 'the_flash_2014')
    },
    'game_of_thrones': {
        'enabled': False,
        'url': 'https://www.tusubtitulo.com/show/770',
        'location': os.path.join(SUBTITLES_FINAL_LOCATION, 'game_of_thrones')
    },
    'haven': {
        'enabled': False,
        'url': 'https://www.tusubtitulo.com/show/620',
        'location': os.path.join(SUBTITLES_FINAL_LOCATION, 'haven')
    },
    'shield': {
        'enabled': True,
        'url': 'https://www.tusubtitulo.com/show/1852',
        'location': os.path.join(SUBTITLES_FINAL_LOCATION, 'marvel\'s_agents_of_s_h_i_e_l_d')
    },
    'mr_robot': {
        'enabled': False,
        'url': 'https://www.tusubtitulo.com/show/2442',
        'location': os.path.join(SUBTITLES_FINAL_LOCATION, 'mr_robot')
    },
    'once_upon_a_time': {
        'enabled': True,
        'url': 'https://www.tusubtitulo.com/show/1116',
        'location': os.path.join(SUBTITLES_FINAL_LOCATION, 'once_upon_a_time')
    },
    'sherlock': {
        'enabled': True,
        'url': 'https://www.tusubtitulo.com/show/635',
        'location': os.path.join(SUBTITLES_FINAL_LOCATION, 'sherlock')
    },
    'silicon_valley': {
        'enabled': True,
        'url': 'https://www.tusubtitulo.com/show/2048',
        'location': os.path.join(SUBTITLES_FINAL_LOCATION, 'silicon_valley')
    },
    'supergirl': {
        'enabled': True,
        'url': 'https://www.tusubtitulo.com/show/2438',
        'location': os.path.join(SUBTITLES_FINAL_LOCATION, 'supergirl')
    },
    'supernatural': {
        'enabled': False,
        'url': 'https://www.tusubtitulo.com/show/12',
        'location': os.path.join(SUBTITLES_FINAL_LOCATION, 'supernatural')
    },
    'under_the_dome': {
        'enabled': False,
        'url': 'https://www.tusubtitulo.com/show/1747',
        'location': os.path.join(SUBTITLES_FINAL_LOCATION, 'under_the_dome')
    },
    'the_walking_dead': {
        'enabled': False,
        'url': 'https://www.tusubtitulo.com/show/750',
        'location': os.path.join(SUBTITLES_FINAL_LOCATION, 'the_walking_dead')
    }
}
