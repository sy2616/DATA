# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CsdnpaperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title_url=scrapy.Field()
    title=scrapy.Field()
    content=scrapy.Field()
    time=scrapy.Field()