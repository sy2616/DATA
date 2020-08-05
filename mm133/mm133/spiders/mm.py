import scrapy
from mm133.items import Mm133Item

class MmSpider(scrapy.Spider):
    name = 'mm'
    allowed_domains = ['www.mm131.com']
    start_urls = ['http://www.mm131.com/xinggan/',
                  'http://www.mm131.com/qingchun/',
                  'http://www.mm131.com/xiaohua/',
                  'http://www.mm131.com/chemo/',
                  'http://www.mm131.com/qipao/',
                  'http://www.mm131.com/mingxing/']

    def parse(self, response):
        #print(response.text)
        list=response.css('.list-left dd:not(.page')
        for img in list:
            imgname=img.css('a::text').get()
            imgurl=img.css('a::attr(href)').get()
            imgurl2=str(imgurl)
            next_page=response.css('.page-en:nth-last-child(2)::attr(href)').get()
            if next_page is not None:
                yield response.follow(next_page,callback=self.parse)
            yield scrapy.Request(imgurl2,callback=self.content)
    
    def content(self,response):
        item=Mm133Item()
        item['name']=response.css('.content h5::text').get()
        item['nameurl']=response.css('.content-pic img::attr(src)').getall()
        yield item
        next_url=response.css('.page-ch:last-child::attr(href)').get()
        if next_url is not None:
            yield response.follow(next_url,callback=self.content)
            