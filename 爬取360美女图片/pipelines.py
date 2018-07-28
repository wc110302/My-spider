# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging

import scrapy
from pymongo import MongoClient
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy.conf import settings
from myimage.settings import *


logger = logging.getLogger('SaveImagePipeline')


class SaveImagePipeline(ImagesPipeline):
    # 重构三个方法
    def get_media_requests(self, item, info):
        logging.debug('图片下载完成')
        yield scrapy.Request(url=item['url'])

    def item_completed(self, results, item, info):
        if not results[0][0]:
            raise DropItem('下载失败')
        return item

    def file_path(self, request, response=None, info=None):
        # 拆分文件名
        return request.url.split('/')[-1]

class MongoPipeline(object):

    def __init__(self):
        self.mongo_url = MONGO_URL
        self.db_name = MONGO_DB


    def process_item(self, item, spider):

        mylist = [{
            'title': item['title'],
            'tag': item['tag'],
            'width': item['width'],
            'height': item['height'],
            'url': item['url']
        }]
        self.db['item'].insert(mylist)

        return item

    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_url)
        self.db = self.client[self.db_name]

    def close_spider(self, spider):
        self.client.close()

    # @classmethod
    # def from_crawler(cls, crawler):
    #
    #     return cls(crawler.settings.get['MONGO_URL'],
    #                crawler.settings.get['MONGO_DB'],)