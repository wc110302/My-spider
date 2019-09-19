import re
import json
import time

import requests
from lxml import etree

from localOcr import join, get_num


def getProxies():
    """
    Please use your proxies
    :return: proxies
    """


class Citeab(object):
    def __init__(self, url):
        self.s = requests.Session()
        self.url = url
        self.proxies = getProxies()
        self.timeout = 10

    def get_html(self, count):

        headers = {
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Encoding":"gzip, deflate, br",
                "Accept-Language":"zh-CN,zh;q=0.9",
                "Connection":"keep-alive",
                "Host":"www.citeab.com",
                "Upgrade-Insecure-Requests":"1",
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
        }

        r = self.s.get(self.url, headers=headers, proxies=self.proxies, timeout=self.timeout)

        cs_token = re.findall('<meta name="csrf-token" content="(.*?)" />', r.text)[0]  # csrf破解

        headers1 = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Host": "www.citeab.com",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
            "X-CSRF-Token": cs_token,
            "If-None-Match": 'W/"d4dfc7c5f80c37bed2d83a45b13111d2"',
            "Referer": self.url,
        }

        r = self.s.get('https://www.citeab.com/session/challenge', headers=headers1, proxies=self.proxies, timeout=self.timeout)

        selector = etree.HTML(r.text)

        token = re.findall("<img src='/sesson/challenge/image/.*\?token=(.*?)'>", r.text)[0]  # token参数获取

        imgs = selector.xpath('//div[@class="captcha-question"]/img/@src')

        imgs1 = ["https://www.citeab.com" + i for i in imgs]  # 图片获取

        for i in range(len(imgs1)):
            r = self.s.get(imgs1[i], headers=headers, proxies=self.proxies, timeout=self.timeout)
            with open('./image_{1}/{0}.jpg'.format(str(i), str(count)), 'wb') as f:
                f.write(r.content)

        join('./image_{0}/0.jpg'.format(str(count)), './image_{0}/1.jpg'.format(str(count)), './image_{0}/2.jpg'.format(str(count)), './image_{0}/3.jpg'.format(str(count)), count) # 图片拼接

        answer = get_num('./image_{0}/7.png'.format(str(count)))  # 调用本地库识别图片并计算答案

        data = {
            "token": token,
            "answer": answer
        }

        print(data)
        print(count)
        self.s.post('https://www.citeab.com/session/check_answer', headers=headers1, data=data, proxies=self.proxies, timeout=self.timeout)

        r = self.s.get(self.url, headers=headers, proxies=self.proxies, timeout=self.timeout)

        selector1 = etree.HTML(r.text)
        print(r.text)
        des = re.findall("<div class='search-results' data-des='(.*?)'>", r.text)[0]
        detail_url = "https://www.citeab.com" + selector1.xpath('//div[contains(@class, "name")]/a/@href')[0] + "?des=" + des
        r = self.s.get(detail_url, headers=headers, proxies=self.proxies, timeout=self.timeout)
        print(r.headers)
        print(r.url)
        print(r.status_code)
        print(r.cookies.get_dict())
        mystr = ''
        mydict = r.cookies.get_dict()
        for i in mydict.keys():
            mystr += (i + '=' + mydict[i] + ';')
        self.cookie = mystr
        print(mystr)
        return r.text  # 详情页的html

    def use_cookie_get_html(self, url):  # 减少打码开支 利用cookie继续获取html
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Cookie": self.cookie,
            "Host": "www.citeab.com",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
        }

        r = self.s.get(url, headers=headers, proxies=self.proxies, timeout=self.timeout)
        selector1 = etree.HTML(r.text)

        des = re.findall("<div class='search-results' data-des='(.*?)'>", r.text)[0]
        detail_url = "https://www.citeab.com" + selector1.xpath('//div[contains(@class, "name")]/a/@href')[0] + "?des=" + des
        r = self.s.get(detail_url, headers=headers, proxies=self.proxies, timeout=self.timeout)
        print(r.text)
        return r.text


if __name__ == '__main__':
    url = 'https://www.citeab.com/antibodies/search?q=SAB3700197'
    Cb = Citeab(url)
    html = Cb.get_html(1)
    print(html)
