# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings
from scrapy import log


class JobsPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        #Remove invalid data

        #Insert data into database
        new_job=[{
            "job": item['job'],
            "money": item['money'],
            "addr": item['addr'],
            "company": item['company'],
            "needs": item['needs'],
            "content": item['content'],
            "work_addr": item['work_addr'],

        }]
        self.collection.insert(new_job)
        log.msg("Item wrote to MongoDB database %s/%s" %
        (settings['MONGODB_DB'], settings['MONGODB_COLLECTION']),
        level=log.DEBUG, spider=spider)

        return item
