# -*- coding: utf-8 -*-

from scrapy.http import Request
from scrapy.pipelines.files import FilesPipeline


class DownloadSubtitlePipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        return [
            Request(url, headers={
                # 'Referer': item['show_url']
                'Referer': url
            })
            for url in item.get(self.files_urls_field, [])
        ]
