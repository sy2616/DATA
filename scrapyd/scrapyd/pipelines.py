# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.utils.project import get_project_settings
import pymongo

class ScrapydPipeline:
    def __init__(self):
        settings=get_project_settings()
        host=settings['MONGODB_URL']
        port=settings['MONGODB_PORT']
        name=settings['MONGODB_NAME']
        sheet=settings['MONGODB_SHEET']

        cilent=pymongo.MongoClient(host,port)
        mydb=cilent[name]
        self.sheet=mydb[sheet]

    def process_item(self, item, spider):
        data=dict(item)
        self.sheet.insert(data)
        return item
