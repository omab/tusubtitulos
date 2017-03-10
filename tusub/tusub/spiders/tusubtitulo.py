# -*- coding: utf-8 -*-
from six.moves.urllib_parse import urlparse

from scrapy import Spider, Request
from scrapy.loader import ItemLoader

from ..items import SubtitleItem


class TusubtituloSpider(Spider):
    name = 'tusubtitulo'
    allowed_domains = [
        'www.tusubtitulo.com'
    ]
    start_urls = [
        # supergirl
        'https://www.tusubtitulo.com/show/2438',
        # the big bang theory
        'https://www.tusubtitulo.com/show/26',
        # the flash
        'https://www.tusubtitulo.com/show/2125'
    ]

    ajax_url = 'https://www.tusubtitulo.com/ajax_loadShow.php?show={show}&season={season}'

    def parse(self, response):
        show = response.url.split('/')[-1]
        season = response.css('#contenido') \
                         .xpath('.//table/tr/td[4]/span/a[last()]//text()') \
                         .extract_first()
        url = self.ajax_url.format(show=show, season=season)
        yield Request(url, self.parse_season, meta={
            'show': show,
            'scheme': urlparse(response.url).scheme,
            'show_url': response.url
        })

    def parse_season(self, response):
        items = []
        show = response.meta.get('show')
        scheme = response.meta.get('scheme')
        show_url = response.meta.get('show_url')
        for table in response.xpath('//table'):
            items += self.parse_episode(show, show_url, scheme, table)
        return items

    def parse_episode(self, show, show_url, scheme, table):
        items = []
        rows = table.xpath('.//tr//td[@class="language"]/..')

        for index, row in enumerate(rows):
            loader = ItemLoader(SubtitleItem(), row)
            loader.add_value('show_url', show_url)
            loader.add_value('show', show)
            loader.add_value('index', index)
            loader.add_css('language', '.language::text')
            loader.add_xpath('status', './/td[6]/text()')
            loader.add_value('file_urls', [
                '{scheme}:{url}'.format(scheme=scheme, url=url)
                for url in row.xpath('.//td[7]/a/@href').extract()
            ])
            items.append(loader.load_item())
        return items
