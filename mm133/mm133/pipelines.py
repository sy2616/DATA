# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import re
from scrapy.exceptions import DropItem
import scrapy

class Mm133Pipeline(ImagesPipeline):
    def get_media_requests(self,item,info):
        for img_url in item['nameurl']:
            yield scrapy.Request(img_url,meta={'item':item['name']})

    def file_path(self,request,response=None,info=None):
        name=request.meta['item']
        name = re.sub(r'[？\\*|“<>:/()0123456789]', '', name)
        image_guid = request.url.split('/')[-1]
        filename = u'full/{0}/{1}'.format(name, image_guid)
        return filename

    #def process_item(self, item, spider):
     #   return item
    def item_completed(self,results,item,info):
        image_path = [x['path'] for ok, x in results if ok]
        if not image_path:
            raise DropItem('Item contains no images')
        item['image_paths'] = image_path
        return item