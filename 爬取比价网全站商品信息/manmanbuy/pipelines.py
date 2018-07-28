# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
# from manmanbuy.settings import MONGO_URL, MONGO_DB
from scrapy.conf import settings

class ManmanbuyPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):
    def __init__(self):
        # self.mongo_url = MONGO_URL
        # self.mongo_db = MONGO_DB
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]


    # 使用了scrapy-redis这个用不了
    # @classmethod
    # def from_crawl(cls, crawl):
    #     return cls(mongo_url=crawl.settings.get('MONGO_URL'),
    #                mongo_db=crawl.settings.get('MONGO_DB'))

    # def open_spider(self, spider):
    #     self.connect = pymongo.MongoClient(self.mongo_url)
    #     self.db = self.connect[self.mongo_db]

    def process_item(self, item, spider):
        new_item = [{
            'name': item['name'],
            'c_price': item['c_price'],
            'image': item['image'],
            'description': item['description'],
            'comments_amount': item['comments_amount'],
            'sales_number': item['sales_number'],
            'source': item['source'],
            'url': item['url'],
            'brand': item['brand'],
            'subclassification': item['subclassification'],
            'classification': item['classification'],
        }]
        self.collection.insert(new_item)
        return item

    # def close_spider(self, spider):
    #     self.connect.close()


