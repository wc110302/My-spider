# -*- coding: utf-8 -*-
# Author：442891187@qq.com
# Date ：2020/4/22 10:11
# Tool ：PyCharm
# Link: https://blog.csdn.net/qq_39802740/article/details/104911315
import urllib

import requests


def get_json():
    """
    获取指定作者ID下的文章 可翻页
    :return:
    """
    url = "https://www.toutiao.com/c/user/article/"
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
        "referer": "https://www.toutiao.com/ch/news_tech/",
    }
    params = {
        "page_type": "0",
        "user_id": "2845250445",
        "max_behot_time": "0",
        "as": "",
        "cp": "",
    }
    decode_url = url + "?" + urllib.parse.urlencode(params)
    decode_url = decode_url.replace("com/", "com/toutiao/")
    data = {
        "url": urllib.parse.quote(decode_url)
    }
    _signature = requests.post('http://121.40.96.182:4007/get_sign', data=data).json()['_signature']  # 此为短的加密参数 随机免费开放
    # _signature = requests.post('http://122.51.73.246:4008/get_sign', data=data).json()['_signature'] # 此为长的加密参数 随机免费开放
    print("计算_signature值为：", _signature)
    params["_signature"] = _signature
    resp = requests.get(url, headers=headers, params=params)
    print(resp.json())


if __name__ == '__main__':
    get_json()