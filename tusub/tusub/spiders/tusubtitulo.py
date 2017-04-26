# -*- coding: utf-8 -*-
from six.moves.urllib_parse import urlparse

from guessit import guessit

from scrapy import Spider, Request
from scrapy.loader import ItemLoader

from ..items import SubtitleItem


class TusubtituloSpider(Spider):
    """Tusubtitulo.com crawler"""
    name = 'tusubtitulo'
    allowed_domains = [
        'www.tusubtitulo.com'
    ]
    start_urls = [
        # 12 monkeys
        'https://www.tusubtitulo.com/show/2320',
        # arrow
        'https://www.tusubtitulo.com/show/1493',
        # the big bang theory
        'https://www.tusubtitulo.com/show/26',
        # the blacklist
        'https://www.tusubtitulo.com/show/1832',
        # blindspot
        'https://www.tusubtitulo.com/show/2515',
        # continuum
        'https://www.tusubtitulo.com/show/1336',
        # dc's legends of tomorrow
        'https://www.tusubtitulo.com/show/2651',
        # dr who
        'https://www.tusubtitulo.com/show/117',
        # falling skies
        'https://www.tusubtitulo.com/show/967',
        # the flash
        'https://www.tusubtitulo.com/show/2125',
        # game of thrones
        'https://www.tusubtitulo.com/show/770',
        # haven
        'https://www.tusubtitulo.com/show/620',
        # shield
        'https://www.tusubtitulo.com/show/1852',
        # mr robot
        'https://www.tusubtitulo.com/show/2442',
        # once upon a time
        'https://www.tusubtitulo.com/show/1116',
        # sherlock
        'https://www.tusubtitulo.com/show/635',
        # silicon valley
        'https://www.tusubtitulo.com/show/2048',
        # supergirl
        'https://www.tusubtitulo.com/show/2438',
        # supernatural
        'https://www.tusubtitulo.com/show/12',
        # under the dome
        'https://www.tusubtitulo.com/show/1747',
        # the walking dead
        'https://www.tusubtitulo.com/show/750'
    ]

    ajax_url = 'https://www.tusubtitulo.com/ajax_loadShow.php?show={show}&season={season}'

    @property
    def saved_cache(self):
        """Saved subtitles cache"""
        return getattr(self, '_cache')

    @saved_cache.setter
    def saved_cache(self, value):
        """Set saved subtitles cache"""
        setattr(self, '_cache', value)

    def cached(self, name):
        """Return if we already downloaded a subtitle for the given
        title"""
        guess = guessit(name)
        title = guess['title'].lower()
        season = str(guess['season'])
        episode = int(guess['episode'])
        return episode in self.saved_cache.get(title, {}).get(season, [])

    def parse(self, response):
        """Parse main response"""
        show = response.url.split('/')[-1]
        season = response.css('#content') \
                         .xpath('.//table/tr/td[4]/span/a[last()]//text()') \
                         .extract_first()
        url = self.ajax_url.format(show=show, season=season)
        yield Request(url, self.parse_season, meta={
            'show': show,
            'scheme': urlparse(response.url).scheme,
            'show_url': response.url
        })

    def parse_season(self, response):
        """Parse season"""
        for table in response.xpath('//table'):
            link = table.xpath('.//tr[1]/td[@class="NewsTitle"]/a')
            name = link.xpath('text()').extract_first()

            if self.cached(name):
                continue

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
        """Parse episode"""
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
