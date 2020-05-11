# -*- coding: utf-8 -*-
# Author：442891187@qq.com
# Date ：2020/5/11 14:47
# Tool ：PyCharm
# Link: https://blog.csdn.net/qq_39802740/article/details/106059888
import requests

ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'

headers = {
    "User-Agent": ua,
}

s = requests.Session()
url = 'https://www.toutiao.com/i6824014300391145991/'

resp = s.get(url, headers=headers)
print(resp.text)
resp_cookie = resp.cookies.get_dict()
x = resp_cookie['__ac_nonce']

print(x)

data = {
    "cookie": x
}
r = requests.post('http://121.40.96.182:4006/get_sign', data=data) # 此为__ac_signature参数专属接口 随机免费开放
__ac_signature = r.json()['signature']
Cookie = '__ac_nonce=' + x + '; ' + '__ac_signature='+ __ac_signature
print(Cookie)
headers.update(
    {
        "Cookie": Cookie
    }
)

resp = s.get(url=url, headers=headers).text
print(resp)
