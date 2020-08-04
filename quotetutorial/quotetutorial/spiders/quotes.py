import scrapy
from quotetutorial.items import QuotetutorialItem

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        quotes=response.css('.quote')
        for quote in quotes:
            item=QuotetutorialItem()
            text=quote.css('.text::text').extract()[0]
            author=quote.css('.author::text').extract()[0]
            tags=quote.css('.tags .tag::text').extract()
            item['text']=text
            item['author']=author
            item['tags']=tags
            yield item

        next=response.css('.pager .next a::attr(href)').extract_first()
        url=response.urljoin(next)
        yield scrapy.Request(url=url,callback=self.parse)


