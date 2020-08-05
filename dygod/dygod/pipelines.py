# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo

class DygodPipeline(object):
    #def process_item(self, item, spider):
        #return item
    def __init__(self):
        client=pymongo.MongoClient(host='127.0.0.1',port=27017)
        db=client['dytt']
        self.dbsheet=db['dytt88']
    
    def process_item(self,item,spider):
        sheet=dict(item)
        self.dbsheet.insert(sheet)
        return item