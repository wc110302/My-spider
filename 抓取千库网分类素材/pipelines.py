# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import logging

import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy.conf import settings

logger = logging.getLogger('SaveImagePipeline')


class SaveImagePipeline(ImagesPipeline):
    # 重构三个方法
    def get_media_requests(self, item, info):
        logging.debug('图片下载完成')
        yield scrapy.Request(url=item['src'], meta={'item':item})

    def item_completed(self, results, item, info):
        if not results[0][0]:
            raise DropItem('下载失败')
        return item

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        # 拆分文件名
        file_name = request.url.split('/')[7].split('!')[0]
        final_path = u'{0}/{1}'.format(item['path'], file_name)
        return final_path


