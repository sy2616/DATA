# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import scrapy,re

class ImagePipeline(ImagesPipeline):
    def get_media_requests(self,item,info):
        for img in item['imgurl']:
            yield scrapy.Request(img,meta={'name':item['imgname']})
    
    def file_path(self,request,response=None,info=None):
        img_name=request.url.split('/')[-1]
        name=request.meta['name']
        name=re.sub(r'[？\\*|“<>:/]','',name)
        filename=u'{0}/{1}'.format(name,img_name)
        return filename

    #def process_item(self, item, spider):
        #return item
