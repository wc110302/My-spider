# -*- coding: utf-8 -*-
from json import loads
from urllib.parse import urlencode
import scrapy

from myimage.items import MyimageItem


class ImageSpidr(scrapy.Spider):
    name = 'myimage'
    allowed_domains = ['image.so.com']

    def start_requests(self):
        base_url = 'http://image.so.com/zj?'
        param = {'ch': 'beauty', 'listtype': 'new', 'temp': 1}
        for page in range(10):
            param['sn'] = page * 30
            full_url = base_url + urlencode(param)
            yield scrapy.Request(url=full_url, callback=self.parse)


    def parse(self, response):
        model_dict = loads(response.text)
        for elem in model_dict['list']:
            item = MyimageItem()
            item['title'] = elem['group_title']
            item['tag'] = elem['tag']
            item['width'] = elem['cover_width']
            item['height'] = elem['cover_height']
            item['url'] = elem['qhimg_url']
            yield item