# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import PicItem

file_path = ''

class PictureSpider(CrawlSpider):
    name = 'picture'
    allowed_domains = ['https://588cu.com']

    def start_requests(self):
        base_url = 'http://588ku.com/sucai/0-default-0-0-{0}-0-{1}/'
        list1 = ["dongmanrenwu", "fengjingmanhua", "chuantongwenhua", "tiyuyundong", "huihuashufa",
                "beijingdiwen", "huabianhuawen", "biankuangxiangkuang", "ziranfengguang", "renwenjingguan",
                "jianzhuyuanlin", "yeshengdongwu", "jiaqinjiaxu", "yulei", "shenghuoyongpin", "canyinmeishi",
                "tiyuyongpin", "kexueyanjiu", "gongyeshengchan", "jiaotonggongju", "shangyechahua",
                "shangwuchangjing", "qita", "baozhuangsheji", "zhaotiesheji", "huacesheji"]

        for keyword in list1: # 拼接url
            global file_path
            file_path = keyword
            for page in range(1, 5):
                full_url = base_url.format(keyword, page)
                yield scrapy.Request(full_url, self.parse)

    def parse(self, response):
        pic_list = response.xpath('//*[@id="orgImgWrap"]/div')
        for i in pic_list:
            item = PicItem()
            item['src'] = i.xpath('div[1]/a/img/@data-original').extract_first() # 图片地址
            item['path'] = file_path # 图片分类
            yield item
