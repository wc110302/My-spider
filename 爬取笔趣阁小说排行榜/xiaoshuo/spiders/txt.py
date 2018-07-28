# -*- coding: utf-8 -*-
import scrapy
import re
from xiaoshuo.items import XiaoshuoItem

class TxtSpider(scrapy.Spider):
    name = 'txt'
    allowed_domains = ['http://www.biquge.com.tw/']
    start_urls = ['http://www.biquge.com.tw/paihangbang/']

    def parse(self, response):
        i = response.xpath("//*[@id='main']/div[contains(@class, 'box')]")
        for a in i:
            b = a.xpath('ul/li')
            for x in b:
                url = x.xpath('a/@href').extract_first()
                yield scrapy.Request(url, self.content, dont_filter=True)

    def content(self, response):
        urls = response.xpath('//*[@id="list"]/dl/dd')
        for url in urls:
            item = XiaoshuoItem()
            item['title'] = response.xpath('//*[@id="info"]/h1/text()').extract_first()
            author = response.xpath('//*[@id="info"]/p[1]/text()').extract_first()
            item['author'] = re.sub(r'\xa0|\n|\r', '', author)
            item['last'] = response.xpath('//*[@id="info"]/p[3]/text()').extract_first()
            body_url = url.xpath('a/@href').extract_first()
            body_url = 'http://www.biquge.com.tw' + body_url
            request = scrapy.Request(body_url, self.body, dont_filter=True)
            request.meta['item'] = item
            yield request

    def body(self, response):
        item = response.meta['item']
        title = response.xpath('//*[@class="bookname"]/h1/text()').extract_first()
        item['heading'] = title
        body = response.xpath('//*[@id="content"]//text()').extract()
        item['body'] = ''
        content = ''
        for i in body:
            content += re.sub(r'\xa0|\n|\r', '', i)
        item['body'] += title + content
        yield item


