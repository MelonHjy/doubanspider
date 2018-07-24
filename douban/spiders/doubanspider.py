from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider
from douban.items import DoubanItem


class Douban(CrawlSpider):
    name = 'douban'
    redis_key = 'douban:start_urls'
    start_urls = ['http://movie.douban.com/top250']

    url = 'http://movie.douban.com/top250'

    def parse(self, response):
        item = DoubanItem()
        selector = Selector(response)
        Movies = selector.xpath('//div[@class="info"]')
        for movie in Movies:
            titles = movie.xpath('div[@class="hd"]/a/span/text()').extract()
            fullTitle = ''
            for each in titles:
                fullTitle += each
            movieInfo = movie.xpath('div[@class="bd"]/p/text()').extract()
            star = movie.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').extract()
            quote = movie.xpath('div[@class="bd"]/div[@class="quote"]/span/text()').extract()
            # quote可能为空
            if quote:
                quote = quote[0]
            else:
                quote = ''
            item['title'] = fullTitle
            item['movieInfo'] = ';'.join(movieInfo)
            item['star'] = star
            item['quote'] = quote
            yield item
        nextLink = selector.xpath('//span[@class="next"]/link/@href').extract()
        if nextLink:
            nextLink = nextLink[0]
            print(nextLink)
            yield Request(self.url + nextLink, callback=self.parse)
