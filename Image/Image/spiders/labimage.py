import scrapy
from Image.items import ImageItem

class LabimageSpider(scrapy.Spider):
    name = 'labimage'
    allowed_domains = ['lab.scrapyd.cn']
    start_urls = ['http://lab.scrapyd.cn/archives/55.html',
    'http://lab.scrapyd.cn/archives/57.html']

    def parse(self, response):
        #print(response.text)
        item=ImageItem()
        item['imgurl']=response.xpath('//div[@class="post-content"]/p/img/@src').getall()
        item['imgname']=response.xpath('//h1[@class="post-title"]/a/text()').get()
        yield item