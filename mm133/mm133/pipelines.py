# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy 
import pymongo
from scrapy.pipelines.images import ImagesPipeline

class Mm133Pipeline(ImagesPipeline):
    # def __init__(self):
    #     clien=pymongo.MongoClient(host='127.0.0.1',port=27017)
    #     db=clien['mm']
    #     self.sheet=db['mm131']
    
    def get_media_requests(self,item,info):
        # for img in item['nameurl']:
        img=item['nameurl']
        yield scrapy.Request(url=img)
    
    # def file_path(self,request,response=None,info=None):
    #     name=request.meta['item']
    #     name=re.sub('r[?\\*|“<>:/()0123456789]','',name)
    #     imge_name=request.url.split('/')[-1]
    #     filename=u'full/{0}/{1}'.format(name,imge_name)
    #     return filename
    
    # def item_completed(self,results,item,info):
    #     imagepath=[x['path'] for ok, x in results if ok]
    #     if not imagepath:
    #         raise DropItem('Item contains no images')
    #     item['imagepath']=imagepath
    #     return item
class MmPipeline(object):
    def __init__(self):
        clien=pymongo.MongoClient(host='127.0.0.1',port=27017)
        db=clien['mm']
        self.sheet=db['mm131']
    
    def process_item(self, item, spider):
        detail=dict(item)
        self.sheet.insert(detail)
        return item
