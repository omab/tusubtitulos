# -*- coding: utf-8 -*-

from scrapy import Item, Field

from scrapy.loader.processors import TakeFirst, Join, Compose


def first(value):
    return value[0]

def strip(value):
    return value.strip()

def lower(value):
    return value.lower()


cleaner = Compose(first, strip, lower)


class SubtitleItem(Item):
    show_url = Field(output_processor=cleaner)
    show = Field(output_processor=TakeFirst())
    name = Field(output_processor=cleaner)
    index = Field(output_processor=TakeFirst())
    language = Field(output_processor=cleaner)
    file_urls = Field()
    files = Field()
