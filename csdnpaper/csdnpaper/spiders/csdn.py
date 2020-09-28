import scrapy
from csdnpaper.items import CsdnpaperItem

class CsdnSpider(scrapy.Spider):
    name = 'csdn'
    allowed_domains = ['csdn.net']
    start_urls = ['https://blog.csdn.net/weixin_43067754']

    def parse(self, response):
        ress=response.css('#mainBox main div.article-list div[class*="article-item-box"]')
        for res in ress:
            title_url=res.css('h4 a::attr(href)').get()
            yield scrapy.Request(title_url,callback=self.cotent)
        for i in range(2,8):
            next_url='https://blog.csdn.net/weixin_43067754/article/list/%d'%i
            yield scrapy.Request(next_url,callback=self.parse)

    def cotent(self,response):
        item=CsdnpaperItem()
        item['title']=response.xpath('//*[@id="articleContentId"]/text()').get().strip()
        item['time']=response.css('#mainBox > main > div.blog-content-box > div.article-header-box > div > div.article-info-box > div.article-bar-top > div > span.time::text').get()
        item['content']=response.css('#article_content').get()
        yield item




