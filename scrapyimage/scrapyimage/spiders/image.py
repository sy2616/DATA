import scrapy
from scrapyimage.items import ScrapyimageItem

class ImageSpider(scrapy.Spider):
    name = 'image'
    allowed_domains = ['lab.scrapyd.cn']
    start_urls = ['http://lab.scrapyd.cn/archives/55.html']

    def parse(self, response):
        item=ScrapyimageItem()
        item['imageurl']=response.css('.post-content p img::attr(src)').getall()
        yield item
    
