# -*- coding: utf-8 -*-
import re
import scrapy
from jobs.items import JobsItem

myhref = set()
mylist = set()

class A51jobSpider(scrapy.Spider):
    name = '51job'
    allowed_domains = ['www.51job.com']
    start_urls = ['https://search.51job.com/list/060000,000000,0000,00,9,99,Python,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=']

    def parse(self, response):
        urls = response.xpath('//*[@id="resultList"]/div/p/span/a')
        for url in urls:
            href = url.xpath('@href').extract_first()
            if href and href not in myhref:
                myhref.add(href)
                request = scrapy.Request(url=href, callback=self.mycontent, dont_filter=True)
                yield request

        next_urls = response.xpath('//*[@id="resultList"]/div[55]/div/div/div/ul/li')
        for next_url in next_urls:
            nextUrl = next_url.xpath('a/@href').extract_first()
            if nextUrl and nextUrl not in mylist:
                mylist.add(nextUrl)
                yield response.follow(nextUrl, callback=self.parse, dont_filter=True)

    def mycontent(self, response):
        item = JobsItem()
        need_list = []
        content_list = []
        item['job'] = response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/h1/text()').extract_first()
        item['money'] = response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/strong/text()').extract_first()
        item['addr'] = response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/span/text()').extract_first()
        item['company'] = response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[1]/a/@title').extract_first()
        needs = response.xpath('/html/body/div[3]/div[2]/div[3]/div[1]/div/div/span')
        for need in needs:
            need_list.append(need.xpath('text()').extract_first())
        item['needs'] = need_list
        contents = response.xpath('/html/body/div[3]/div[2]/div[3]/div[2]/div/p')
        for content in contents:
            content1 = content.xpath('text()').extract_first()
            if not content1:
                content1 = content.xpath('span/text()').extract_first()
                if not content1:
                    content1 = '暂无信息'
            content_list.append(content1)
        item['content'] = content_list
        data = response.xpath('/html/body/div[3]/div[2]/div[3]/div[3]/div/p')
        # 这里的p标签下面还有其他标签，用text()不能拿出全部文本，所以用string(.)
        work_addr = data.xpath('string(.)').extract_first()
        # 用正则表达式将\t \n \r 全部去掉 r表示转移原生字符
        item['work_addr'] = re.sub(r'\t|\n|\r', '', work_addr)
        yield item