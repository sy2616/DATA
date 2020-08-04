# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo
# from itemadapter import ItemAdapter
# from scrapy.exceptions import DropItem
from scrapy.utils.project import get_project_settings
settings=get_project_settings()

class TextPipeline(object):
    def __init__(self):
        host=settings['MONGO_URL']
        db=settings['MONGO_DB']
        sheetname=settings['MONGO_SHEETNAME']

        client=pymongo.MongoClient(host)
        mydb=client[db]
        self.sheet=mydb[sheetname]
    def process_item(self,item,spider):
        data=dict(item)
        self.sheet.insert(data)
        return item

        #     def __init__(self):
#         self.limit=50

#   def process_item(self, item, spider):
#         if item['text']:
#             if len(item['text'])>self.limit:
#                 item['text']=item['text'][0:self.limit].rstrip()+'...'
#                 return item
#         else:
#             return DropItem('Missing Text')
# #
# class MongoPipeline(object):
#     def __init__(self,mongo_url,mongo_db):
#         self.mongo_url=mongo_url
#         self.mongo_db=mongo_db
#
#     @classmethod
#     def from_crawler(cls,crawler):
#         return cls(
#             mongo_url=crawler.settings.get('MONGO_URL'),
#             mongo_db=crawler.settings.get('MONGO_DB')
#         )
#     def open_spider(self,spider):
#         self.client=pymongo.MongoClient(self.mongo_url)
#         self.db=self.client[self.mongo_db]
#
#     def process_item(self,item,spider):
#         name=item._class_._name_
#         self.db[name].insert(dict(item))
#         return item
#     def close_spider(self,spider):
#         self.client.close()
#     myclient=pymongo.MongoClient('MONGO_URL')
#     my_db=myclient['MONGO_DB']
#     sheetname=






