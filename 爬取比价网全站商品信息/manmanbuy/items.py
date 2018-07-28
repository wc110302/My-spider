# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ManmanbuyUrls(scrapy.Item):
    urls = scrapy.Field()


class ManmanbuyItem(scrapy.Item):
    name = scrapy.Field()
    c_price = scrapy.Field()
    image = scrapy.Field()
    url = scrapy.Field()
    description = scrapy.Field()
    comments_amount = scrapy.Field()
    sales_number = scrapy.Field()
    source = scrapy.Field()
    brand = scrapy.Field()
    classification = scrapy.Field()
    subclassification = scrapy.Field()

