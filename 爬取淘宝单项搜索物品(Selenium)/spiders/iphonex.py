# -*- coding: utf-8 -*-
from json import loads
from urllib.parse import urlencode
import scrapy

from ipad.items import IpadItem


class ImageSpidr(scrapy.Spider):
    name = 'iphonex'
    allowed_domains = ['taobao.com']

    def start_requests(self):
        # https: // s.taobao.com / search?q = iphonex & s = 45
        # base_url = 'https://s.taobao.com/search?q=iphonex&s='
        # a = 0
        # for i in range(100):
        #     a += i * 44
        #     full_url = base_url + a
        #     yield scrapy.Request(full_url, self.parse)
        base_url = 'https://s.taobao.com/search?'
        params = {}
        for keyword in ['ipad', 'iphonex', '小米手机']:
            params['q'] = keyword
            for page in range(10):
                params['s'] = page * 44
                full_url = base_url + urlencode(params)
                yield scrapy.Request(full_url, self.parse)


    def parse(self, response):
        goods_list = response.xpath('//*[@id="mainsrp-itemlist"]/div/div/div[1]/div')
        for i in goods_list:
            item = IpadItem()
            item['price'] = i.xpath('div[2]/div[1]/div[1]/strong/text()').extract_first()
            item['deal'] = i.xpath('div[2]/div[1]/div[2]/text()').extract_first()
            #  此处有坑，由于title前面有个图片，拿出的extract_first()就是第一个\n \n 所以应该用extract()然后取下表
            item['title'] = i.xpath('div[2]/div[2]/a/text()').extract()[2]

            yield item