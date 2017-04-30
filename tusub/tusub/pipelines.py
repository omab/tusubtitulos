# -*- coding: utf-8 -*-
import json
import logging

from os import path
from glob import glob
from shutil import copyfile

from guessit import guessit

from scrapy import settings
from scrapy.http import Request
from scrapy.pipelines.files import FilesPipeline

from .settings import FILES_STORE, \
    SUPPORTED_VIDEO_EXTENSIONS, \
    SUBTITLES_CACHE_FILE, \
    SERIES


logging.getLogger('rebulk.rules').setLevel(logging.WARNING)
logging.getLogger('rebulk.rebulk').setLevel(logging.WARNING)
logging.getLogger('rebulk.processors').setLevel(logging.WARNING)


class DownloadSubtitlePipeline(FilesPipeline):
    """Download subtitle file"""
    def get_media_requests(self, item, info):
        """Override to set a needed header"""
        return [
            Request(url, headers={
                # 'Referer': item['show_url']
                'Referer': url
            })
            for url in item.get(self.files_urls_field, [])
        ]


class AllocateSubtitlePipeline(object):
    """Take the downloaded files and copy to a human-friendly
    structure"""
    paths = [
        # root/serie/S01/Name-S01E02-Title.mkv
        '{path}/[Ss]{season:02d}/' + \
        '*[Ss]{season:02d}[Ee]{episode:02d}*.{extension}',
        # root/serie/S01/Name-S01E02-Title/Name-S01E02-Title.mkv
        '{path}/[Ss]{season:02d}/' + \
        '*[Ss]{season:02d}[Ee]{episode:02d}*/' +
        '*[Ss]{season:02d}[Ee]{episode:02d}*.{extension}'
    ]

    def open_spider(self, spider):
        """Load saved files cache on spider open"""
        try:
            with open(SUBTITLES_CACHE_FILE, 'r') as file:
                spider.saved_cache = json.load(file)
        except FileNotFoundError:
            spider.saved_cache = {}

    def close_spider(self, spider):
        """Save saved files cache on spider close"""
        cache = spider.saved_cache
        for name, seasons in cache.items():
            for season, episodes in seasons.items():
                cache[name][season] = list(set(episodes))

        with open(SUBTITLES_CACHE_FILE, 'w') as file:
            file.truncate()
            json.dump(cache, file, indent=4)

    def process_item(self, item, spider):
        """Process the item downloaded files and store them in a
        better place"""
        for index, file_info in enumerate(item['files']):
            final_path = self.final_path(SERIES[item['config_name']],
                                         item['name'],
                                         index)
            if final_path:
                guess = guessit(item['name'])
                config_name = item['config_name']
                season = str(guess['season'])
                episode = int(guess['episode'])

                if config_name not in spider.saved_cache:
                    spider.saved_cache[config_name] = {}

                if season not in spider.saved_cache[config_name]:
                    spider.saved_cache[config_name][season] = []

                spider.saved_cache[config_name][season].append(episode)
                copyfile(path.join(FILES_STORE, file_info['path']),
                         final_path)

    def final_path(self, serie_conf, name, index):
        """Detect closer video file in destination"""
        guess = guessit(name)

        for ext in SUPPORTED_VIDEO_EXTENSIONS:
            for path_format in self.paths:
                # files exists in that pseudo path
                path_glob = path_format.format(path=serie_conf['location'],
                                               extension=ext,
                                               **guess)
                path_glob = path_glob.replace(' ', '_')
                files = glob(path_glob)
                if files:  # take first
                    file_path, _ = files[0].rsplit('.', 1)
                    return '{path}-{index}.srt'.format(index=index,
                                                       path=file_path)
