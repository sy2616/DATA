# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ImageItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    imgurl=scrapy.Field()
    imgname=scrapy.Field()
