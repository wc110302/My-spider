# -*- coding: utf-8 -*-
import scrapy
from biaoqing.items import BiaoqingItem

class BiaoqingbaoSpider(scrapy.Spider):
    name = 'biaoqingbao'
    allowed_domains = ['fabiaoqing.com/biaoqing']
    start_urls = ['https://www.fabiaoqing.com/biaoqing/']

    def parse(self, response):
        divs = response.xpath('//*[@id="bqb"]/div[1]/div')
        next_url = response.xpath('//div[contains(@class,"pagination")]/a[last()-1]/@href').extract_first()
        base_url = 'https://fabiaoqing.com'
        for div in divs:
            items = BiaoqingItem()
            items['url'] = div.xpath('a/img/@data-original').extract_first()
            items['title'] = div.xpath('a/@title').extract_first()
            yield items
        if next_url:
            url = base_url + next_url
            yield scrapy.Request(url, self.parse, dont_filter=True)