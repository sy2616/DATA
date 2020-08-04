import scrapy
from scrapyd.items import ScrapydItem

class LabSpider(scrapy.Spider):
    name = 'lab'
    allowed_domains = ['lab.scrapyd.cn']
    start_urls = ['http://lab.scrapyd.cn/']

    def parse(self, response):
        #print(response.text)
        details=response.css('.quote')
        for detail in details:
            item=ScrapydItem()
            item['detail']=detail.css('.text::text').get()
            item['author']=detail.css('.author::text').get()
            item['url']=detail.css('a::attr(href)').get()
            item['tag']=detail.css('.tag::text').getall()
            yield item
        next=response.css('.next a::attr(href)').get()
        if next is not None:
            url=response.urljoin(next)
            yield scrapy.Request(url,self.parse)

