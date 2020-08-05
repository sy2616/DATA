# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DygodItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name=scrapy.Field()
    href=scrapy.Field()

class SecendItem(scrapy.Item):
    name=scrapy.Field()
    time=scrapy.Field()
    url=scrapy.Field()

class ThirdItem(scrapy.Item):
    image=scrapy.Field()
    detail=scrapy.Field()
    name=scrapy.Field()
    magnet=scrapy.Field()
