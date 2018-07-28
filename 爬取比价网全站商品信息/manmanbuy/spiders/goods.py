# -*- coding: utf-8 -*-
import scrapy
from manmanbuy.items import ManmanbuyItem, ManmanbuyUrls

class GoodsSpider(scrapy.Spider):
    name = 'goods'
    allowed_domains = ['www.manmanbuy.com']
    start_urls = ['http://www.manmanbuy.com/']

    # 解析首页的大分类
    def parse(self, response):
        first_url = response.xpath('/html/body/div[4]/div/div[1]/div[1]/ul/li')
        for p in first_url:
            next_url = p.xpath('div[2]/dl/dd')
            for q in next_url:
                url = 'http://www.manmanbuy.com' + q.xpath('a/@href').extract_first()
                yield scrapy.Request(url=url, callback=self.next_parse, dont_filter=True)

    # 解析小分类/品牌
    def next_parse(self, response):
        brands1 = response.xpath('//*[@id="ctl00_ContentPlaceMain_searchField"]/div[2]/div[1]/div[2]/ul[1]/li')
        brands2 = response.xpath('//*[@id="ctl00_ContentPlaceMain_searchField"]/div[2]/div[1]/div[2]/ul[2]/li')
        classification = response.xpath('//*[@id="allcontentPlace"]/div[1]/div/div[1]/div[1]/h3/text()').extract_first()
        subclassification = response.xpath('//*[@id="allcontentPlace"]/div[1]/div/div[1]/div[2]/a/text()').extract_first()
        # 判断是否存在更多品牌
        if brands2:
            brands1 += brands2
        for brands in brands1:
            if brands.xpath('a/text()').extract_first() == '全部': # 去掉"全部"这个品牌
                continue
            item = ManmanbuyItem()
            item['brand'] = brands.xpath('a/text()').extract_first()
            item['classification'] = classification
            item['subclassification'] = subclassification
            next_url = 'http://www.manmanbuy.com/' + brands.xpath('a/@href').extract_first()
            request = scrapy.Request(url=next_url, callback=self.content, dont_filter=True)
            request.meta['item'] = item
            yield request


    # 解析内容/分页
    def content(self, response):
        # base_url = 'http://www.manmanbuy.com'
        item = response.meta['item']
        urls = response.xpath('//*[@id="ctl00_ContentPlaceMain_prolist"]/div[2]/ul/li')
        for i in urls:
            item['image'] = i.xpath('.//div[contains(@class, "pic")]/a/img/@original').extract_first()
            url = response.urljoin(i.xpath('.//div[contains(@class, "name")]/a/@href').extract_first())
            item['url'] = url
            item['c_price'] = i.xpath('.//div[contains(@class, "price")]//text()').extract()[1]
            item['description'] = i.xpath('.//div[contains(@class, "name")]/a/text()').extract_first()
            item['sales_number'] = i.xpath('.//div[contains(@class, "sales")]/span//text()').extract_first()
            item['comments_amount'] = item['sales_number']
            item['name'] = item['description']
            item['source'] = '比价网'
            # request = scrapy.Request(url=url, callback=self.content, dont_filter=True) # 同使用response.follow()方法
            # request.meta['item'] = item # 指定response给下一个方法, 对应需要取出的每一个数据
            yield item

        # 下一页数据
        next_page_url = response.xpath('//*[@id="dispage"]/a[3]/@href').extract_first()
        if not next_page_url:
            next_page_url = response.xpath('//*[@id="dispage"]/a[1]/@href').extract_first()
        if next_page_url:
            url = "http://www.manmanbuy.com/" + next_page_url
            yield scrapy.Request(url=url, callback=self.content, dont_filter=True)

    # def content(self, response):
    #     item = response.meta['item']
    #     item['name'] = response.xpath('//*[@id="aspnetForm"]/div[3]/div/div[2]/div[1]/h1/text()').extract_first()
    #     goods = response.xpath('//*[@id="aspnetForm"]/div[3]/div/div[6]/div[2]/ul/li')
    #     for x in goods:
    #         item['description'] = x.xpath('div/div[2]/div/a/text()').extract_first()
    #         item['source'] = x.xpath('div/div[1]//p/text()').extract_fitst()
    #         item['c_price'] = x.xpath('div/div[3]/div/span[1]//text()').extract_fitst()
    #         item['comments_amount'] = x.xpath('div/div[5]/a/span/text()').extract_fitst()
    #         yield item
