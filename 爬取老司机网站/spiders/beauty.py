# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from belle.items import BelleItem
from selenium import webdriver

class BeautySpider(CrawlSpider):
    name = 'beauty'
    allowed_domains = ['m.xxxiao.com']
    start_urls = ['http://m.xxxiao.com/']

    # rules = (
    #     Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    # )

    # def __init__(self):
    #     # use any browser you wish
    #     self.browser = webdriver.Chrome() #使用前请安装对应的webdriver
    #
    #
    # def __del__(self):
    #     self.browser.close()



    def parse(self, response):
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        # self.browser.get(response)
        # sampleSet = set()

        belle_list = response.xpath('//*[@id="panel-126683-0-0-1"]/div/div/div/div/div')
        for belle in belle_list:

            href = belle.xpath('article/div/a/@href').extract_first()
            url = response.urljoin(href)
            request = scrapy.Request(url=url, callback=self.content, dont_filter=True)
            yield request


    def content(self, response):
        item = BelleItem()
        imgs = response.xpath('//*[@id="main"]/article/div/div[1]/a')
        item['name'] = response.xpath('//*[@id="breadcrumbs"]/span/span/span/span/strong/text()').extract_first()
        for img in imgs:
            item['ImgUrl'] = img.xpath('@data-src').extract()
            yield item
