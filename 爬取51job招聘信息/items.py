# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JobsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    job = scrapy.Field()
    money = scrapy.Field()
    addr = scrapy.Field()
    company = scrapy.Field()
    needs = scrapy.Field()
    content = scrapy.Field()
    work_addr = scrapy.Field()