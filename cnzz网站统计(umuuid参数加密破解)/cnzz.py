import time
import random
import threading

import execjs
import requests
from fake_useragent import UserAgent


referer_list = ["https://www.baidu.com", "https://www.google.com", "https://www.sogou.com/", "https://m.so.com/", "https://cn.bing.com/", ""]

ua = UserAgent()

headers = {
        "User-Agent": ua.random,
        "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Host": "z1.cnzz.com",
        "Referer": "https://www.mafengwo.cn/",
}

headers1 = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding":"gzip, deflate, br",
    "Accept-Language":"zh-CN,zh;q=0.9",
    "Connection":"keep-alive",
    "Host":"www.woheyun.com",
    "Upgrade-Insecure-Requests":"1",
    "User-Agent": ua.random,
    "Referer": random.choice(referer_list),
}


def go():
    try:
        for _ in range(999999999):
            try:
                s = requests.Session()
                proxies = getFastProxies() # 你的ip代理
                s.get('https://www.mafengwo.cn', headers=headers1, proxies=proxies, timeout=5, allow_redirects=False)
                # print(r.text)
                _js = execjs.compile(open('uuid.js', 'r').read())
                umuuid = _js.call('get_umuuid', headers.get('User-Agent'), int(time.time()))
                print(umuuid)
                r = s.get('https://hqs9.cnzz.com/stat.htm?id=30065558&r=https%3A%2F%2Fwww.mafengwo.cn%2F&lg=zh-cn&ntime={0}&cnzz_eid=1727325957-{0}-https%3A%2F%2Fwww.mafengwo.cn%2F&showp=1920x1080&p=https%3A%2F%2Fwww.mafengwo.cn%2F&t=%E6%97%85%E6%B8%B8%E6%94%BB%E7%95%A5%2C%E8%87%AA%E7%94%B1%E8%A1%8C%2C%E8%87%AA%E5%8A%A9%E6%B8%B8%E6%94%BB%E7%95%A5%2C%E6%97%85%E6%B8%B8%E7%A4%BE%E4%BA%A4%E5%88%86%E4%BA%AB%E7%BD%91%E7%AB%99%20-%20%E9%A9%AC%E8%9C%82%E7%AA%9D&umuuid={2}&h=1&rnd={1}'.format(int(time.time()), random.randint(1000000000, 9999999999), umuuid), headers=headers, proxies=proxies, timeout=5, allow_redirects=False)
                # print(r.text)
                print(r.status_code)
            except Exception as e:
                print(e)
                s = requests.Session()
                proxies = getProxies() # 你的ip代理
                s.get('https://www.mafengwo.cn', headers=headers1, proxies=proxies, timeout=5, allow_redirects=False)
                _js = execjs.compile(open('uuid.js', 'r').read())
                umuuid = _js.call('get_umuuid', headers.get('User-Agent'), int(time.time()))
                print(umuuid)
                r = s.get('https://hqs9.cnzz.com/stat.htm?id=30065558&r=https%3A%2F%2Fwww.mafengwo.cn%2F&lg=zh-cn&ntime={0}&cnzz_eid=1727325957-{0}-https%3A%2F%2Fwww.mafengwo.cn%2F&showp=1920x1080&p=https%3A%2F%2Fwww.mafengwo.cn%2F&t=%E6%97%85%E6%B8%B8%E6%94%BB%E7%95%A5%2C%E8%87%AA%E7%94%B1%E8%A1%8C%2C%E8%87%AA%E5%8A%A9%E6%B8%B8%E6%94%BB%E7%95%A5%2C%E6%97%85%E6%B8%B8%E7%A4%BE%E4%BA%A4%E5%88%86%E4%BA%AB%E7%BD%91%E7%AB%99%20-%20%E9%A9%AC%E8%9C%82%E7%AA%9D&umuuid={2}&h=1&rnd={1}'.format(int(time.time()), random.randint(1000000000, 9999999999), umuuid), headers=headers, proxies=proxies, timeout=5, allow_redirects=False)
                # print(r.text)
                print(r.status_code)
    except:
        go()


threads = []
for num in range(100):  # 100个线程
    threads.append(threading.Thread(target=go, args=()))
print("Go!")
print(len(threads))
for t in threads:
    t.start()
