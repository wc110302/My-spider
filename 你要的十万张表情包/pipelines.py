# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

class BiaoqingPipeline(object):
    def process_item(self, item, spider):
        return item

class BiaoqingbaoPipeline(ImagesPipeline):
    # 重构三个方法
    def get_media_requests(self, item, info):
        yield scrapy.Request(url=item['url'], meta={'title': item['title']})

    def item_completed(self, results, item, info):
        # if not results[0][0]:
        #     raise DropItem('下载失败')
        print(results)
        return item

    def file_path(self, request, response=None, info=None):
        # 拆分文件名
        title = request.meta['title'] + '.' + request.url.split('.')[-1]
        return title
