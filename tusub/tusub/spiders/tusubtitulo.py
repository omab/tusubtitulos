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
        for table in response.xpath('//table'):
            link = table.xpath('.//tr[1]/td[@class = "NewsTitle"]/a')
            name = link.xpath('text()').extract_first()
            url = link.xpath('@href').extract_first()
            url = '{scheme}:{url}'.format(scheme=response.meta['scheme'],
                                          url=url)
            yield Request(url, self.parse_episode, meta={
                'name': name,
                'show': response.meta['show'],
                'show_url': response.meta['show_url'],
                'scheme': response.meta['scheme']
            }, headers={
                'Referer': response.meta['show_url']
            })

    def parse_episode(self, response):
        items = []
        name = response.meta['name']
        show = response.meta['show']
        show_url = response.meta['show_url']
        index = 0

        for section in response.xpath('.//li[@class = "li-idioma"]/..'):
            if section.css('.li-estado.green').extract():
                # subtitle completed
                loader = ItemLoader(SubtitleItem(), section)
                loader.add_value('show_url', show_url)
                loader.add_value('show', show)
                loader.add_value('name', name)
                loader.add_value('index', index)
                loader.add_css('language', '.li-idioma b::text')
                urls = []
                for href in section.css('.download a').xpath('@href').extract():
                    if href.startswith('a/'):
                        continue
                    urls.append(response.urljoin(href))
                loader.add_value('file_urls', urls)
                items.append(loader.load_item())
                index += 1
        return items
