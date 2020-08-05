import scrapy
from dygod.items import DygodItem,SecendItem,ThirdItem

class DyttSpider(scrapy.Spider):
    name = 'dytt'
    allowed_domains = ['www.dygod.net']
    start_urls = ['http://www.dygod.net/']

    def parse(self, response):
        # print(response.text)
        rss=response.css('#menu .contain ul li')
        for i in range(10):
            item=DygodItem()
            if i==1:
                continue
            else:
                item['name']=rss[i].css('a::text').get()
                item['href']=rss[i].css('a::attr(href)').get()
            next_page='http://www.dygod.net'+item['href']
            yield scrapy.Request(next_page,self.SecondParse,meta={'item':item})

    def SecondParse(self,response):
        details=response.css('.co_content8 ul table')
        for detail in details:
            item=SecendItem()
            item['name']=detail.css('b a::text').get()
            item['time']=detail.css('tr td font[color="#8F8C89"]::text').get().split('\r')[0]
            item['url']=detail.css('a::attr(href)').get()
            next_page='http://www.dygod.net'+item['url']
            yield scrapy.Request(next_page,self.ThirdParse,meta={'item':item})

    def ThirdParse(self,response):
        item=ThirdItem()
        item['image']=response.xpath('//*[@id="Zoom"]/img/@src').get()
        item['detail']=response.xpath('//*[@id="Zoom"]/br//text()').getall()
        item['name']=response.css('.co_area2 h1::text').get()
        item['magnet']=response.css('#downlist a::attr(href)').getall()
        yield item

