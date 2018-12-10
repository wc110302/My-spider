import re
import sys

import requests
import gevent,time
from gevent import monkey
from urllib.request import urlopen, Request

import Proxys

monkey.patch_all()
sys.setrecursionlimit(1000000)


def myspider(range1):
    headers = {
        "Host": "wenku.baidu.com",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6788.400 QQBrowser/10.3.2864.400",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Referer": "https://wenku.baidu.com/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }

    urls = []
    if range1 == 50:
        range2 = 1
    else:
        range2 = range1 - 100
    for i in range(range2, range1):
        for x in range(0, 760, 10):
            url = 'https://wenku.baidu.com/search/main?word={0}&org=0&fd=0&lm=1&od=0&pn={1}'.format(i, x)
            urls.append(url)

    wenku_urls = []
    for url in urls:
        print(url)
        try:
            # r = Request(url, headers=headers)
            resp = urlopen(url)
            data = resp.read()
            list1 = re.findall('<a href="(.*)\?from=search', data.decode('gb18030'))
            wenku_urls += list1
            print(list1)
            print(url)
        except Exception as e:
            print(e)
            continue
    print(wenku_urls)
    print(len(wenku_urls))

    with open('{0}.txt'.format(range1//50), 'w', encoding='utf-8') as f:  # 记录urls
        for i in list(set(wenku_urls)):
            f.write(i + '\n')

async_time_start = time.time()

jobs = []
for i in range(50, 25001, 50):
    jobs.append(i)
print(jobs)

job = [gevent.spawn(myspider, range1) for range1 in jobs]
gevent.joinall(job)

print("异步耗时：", time.time() - async_time_start)