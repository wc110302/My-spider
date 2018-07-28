import logging

from hashlib import sha1
from enum import Enum, unique
from queue import Queue
from random import random
from threading import Thread, current_thread
from time import sleep
from urllib.parse import urlparse

import requests
import redis
import pymongo
from bs4 import BeautifulSoup
from bson import Binary


# 不可重复
@unique
# 枚举
class SpiderStatus(Enum):
    IDLE = 0
    WORKING = 1

# 通过指定的字符集对页面进行解码(不是每个网站都将字符集设置为utf-8)
def decode_page(page_bytes, charsets=('utf-8',)):
    page_html = None
    for charset in charsets:
        try:
            page_html = page_bytes.decode(charset)
            break
        except UnicodeDecodeError:
            pass
            # logging.error('Decode:', error)
    return page_html

class Retry(object):

    def __init__(self, *, retry_times=3,
                 wait_secs=5, errors=(Exception, )):
        self.retry_times = retry_times
        self.wait_secs = wait_secs
        self.errors = errors

    def __call__(self, fn):

        def wrapper(*args, **kwargs):
            for _ in range(self.retry_times):
                try:
                    return fn(*args, **kwargs)
                except self.errors as e:
                    print(e)
                    sleep((random() + 1) * self.wait_secs)
            return None

        return wrapper


class Spider(object):

    def __init__(self):
        self.status = SpiderStatus.IDLE

    # 抓取
    @Retry()
    def fetch(self, current_url, *, charsets=('utf-8', ), user_agent=None, proxies=None):
        thread_name = current_thread().name
        # logging.info('[Fetch]' + current_url)
        print(f'[{thread_name}]: {current_url}')
        headers = {'user-agent': user_agent} if user_agent else {}
        resp = requests.get(current_url,
                            headers=headers, proxies=proxies)
        return decode_page(resp.content, charsets)\
            if resp.status_code == 200 else None

    # 解析
    def parse(self, html_page, *, domain='m.sohu.com'):
        soup = BeautifulSoup(html_page, 'lxml')

        for a_tag in soup.body.select('a[href]'):
            parser = urlparse(a_tag.attrs['href'])
            netloc = parser.netloc or domain
            scheme = parser.scheme or 'http'
            if scheme != 'javascript' and netloc == domain:
                path = parser.path
                query = '?' + parser.query if parser.query else ''
                full_url = f'{scheme}://{netloc}{path}{query}'
                if not redis_client.sismember('visited_urls', full_url):
                    redis_client.rpush('m_sohu_url', full_url)

    # 提取
    def extract(self, html_page):
        pass
    # 存储
    def store(self, data_dict):
        pass


# Thread(target=foo, args(,)).start()
class SpiderThread(Thread):

    def __init__(self, name, spider):
        super().__init__(name=name, daemon=True)
        self.spider = spider


    def run(self):
        while True:
            current_url = redis_client.lpop('m_sohu_url')
            while not current_url:
                current_url = redis_client.lpop('m_sohu_url')
            self.spider.status = SpiderStatus.WORKING
            current_url = current_url.decode('utf-8')
            if not redis_client.sismember('visited_urls', current_url):
                redis_client.sadd('visited_urls', current_url)

                html_page = self.spider.fetch(current_url)
                if html_page not in [None, '']:
                    hasher = hasher_proto.copy()
                    hasher.update(current_url.encode('utf-8'))
                    doc_id = hasher.hexdigest()
                    # Binary()
                    if not sohu_data_coll.find_one({'_id': doc_id}):
                        sohu_data_coll.insert_one({
                            '_id':doc_id,
                            'url': current_url,
                            'page': html_page
                        })
                    self.spider.parse(html_page)
            self.spider.status = SpiderStatus.IDLE

def is_any_alive(spider_threads):
    # any/all 任意一个true则为true/ 任意一个false则为false
    return any([spider_thread.spider.status == SpiderStatus.WORKING
                for spider_thread in spider_threads])

redis_client = redis.Redis(host='47.106.122.64', port=23333, password='123456')

mongo_client = pymongo.MongoClient(host='47.106.122.64', port=27017)
db = mongo_client.msohu
sohu_data_coll = db.webpages
hasher_proto = sha1()

def main():
    if not redis_client.exists('m_sohu_url'):
        redis_client.rpush('m_sohu_url', 'http://m.sohu.com/')
    spider_threads = [SpiderThread('thread-%d' % i,Spider())
                      for i in range(10)]
    for spider_thread in spider_threads:
        spider_thread.start()

    while redis_client.exists('m_sohu_url') or is_any_alive(spider_threads):
        pass

    print('Over!')

if __name__ == '__main__':
    main()