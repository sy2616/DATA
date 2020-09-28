# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.files import FilesPipeline
import scrapy

class CsdnpaperPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        yield scrapy.Request(item['content'],meta={'item':item})
    def file_path(self, request, response=None, info=None):
        item=request.meta['item']
        name=item['title']
        filename=u'{}'.format(name)
        return filename

    def process_item(self, item, spider):
        return item
