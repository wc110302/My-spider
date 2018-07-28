# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

class XiaoshuoPipeline(object):
    def process_item(self, item, spider):
        return item


class FetchPipeline(object):

    def process_item(self, item, spider):
        Path = 'F:\笔趣阁小说'
        tempPath = item['title']
        targetPath = Path + os.path.sep + tempPath
        if not os.path.exists(targetPath):
            os.makedirs(targetPath)

        filename = targetPath + os.path.sep + item['heading'] + '.txt'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(item['body'])

        return item
