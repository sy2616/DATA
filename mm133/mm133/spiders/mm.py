import scrapy
from mm133.items import Mm133Item

class MmSpider(scrapy.Spider):
    name = 'mm'
    allowed_domains = ['www.mm131.net']
    start_urls = ['https://www.mm131.net/xinggan/']

    def parse(self, response):
        #print(response.text)
        res=response.css('dl.list-left dd')
        for i in range(len(res)-1):
            title=res[i].css('a img::attr(alt)').get()
            titleurl=res[i].css('a::attr(href)').get()
            #item['title']=title
            # yield item
        # if res[-1].css('.page a::text').get()=='下一页':
        #     next_url='https://www.mm131.net/xinggan/'+res[-1].css('.page a::attr(href)').get()
        #     yield scrapy.Request(url=next_url,callback=self.parse)
        next_url=response.css('body > div.main > dl > dd.page > a:nth-last-child(2)::attr(href)').get()
        if next_url is not None:
            next_url=response.urljoin(next_url)
            yield scrapy.Request(next_url,callback=self.parse)
        yield scrapy.Request(url=titleurl,callback=self.contentparse)

    
    def contentparse(self,response):
        item=Mm133Item()
        #list=[]
        item['name']=response.css('.content h5::text').get()
        # item['name']=response.meta['name']
        # list=[]
        item['nameurl']=response.css('body > div.content > div.content-pic > a > img::attr(src)').get()
        #item['nameurl']=list
        yield item
        next_page=response.css('body > div.content > div.content-page > a.page-ch::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page,callback=self.contentparse)
