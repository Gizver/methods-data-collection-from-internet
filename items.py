# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst
from w3lib.html import remove_tags
import re

def str_to_float(value):
    try:
        value = float(value.replace(' ', ''))
    except ValueError:
        pass
    return value


def remove_spaces_in_options(value):
    if type(value) == dict:
        for k, v in value.items():
            v = v.lstrip()
            v = v.rstrip()
            value[k] = str_to_float(v)

    return value


def link_to_big_photo(value):
    return re.sub(",w_\d*,h_\d*,",",", value)


class GoodsItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(link_to_big_photo))
    description = scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    options = scrapy.Field(input_processor=MapCompose(remove_spaces_in_options), output_processor=TakeFirst())
    link = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(str_to_float), output_processor=TakeFirst())
    _id = scrapy.Field()