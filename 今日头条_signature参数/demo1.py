# -*- coding: utf-8 -*-
# Author：442891187@qq.com
# Date ：2020/4/10 15:10
# Tool ：PyCharm
# Link: https://blog.csdn.net/qq_39802740/article/details/104911315
import urllib

import requests


def get_json():
    """
    获取首页最新讯息
    :return:
    """
    url = "https://www.toutiao.com/api/pc/feed/"
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
        "referer": "https://www.toutiao.com/ch/news_tech/",
        "cookie": "tt_webid=6813180231643842055; s_v_web_id=verify_k8qsa0sp_jEPsi8T0_v8Xq_4vy5_9CGL_lzDlgECaeNas; WEATHER_CITY=%E5%8C%97%E4%BA%AC; tt_webid=6813180231643842055; csrftoken=c8f42aa845360a9eb6cf0cd9822ef2e4; SLARDAR_WEB_ID=7b76e1bd-12ec-4c3b-ad30-6cdf2e38e81c; _ga=GA1.2.1882245732.1586343902; _gid=GA1.2.132314476.1586343902; tt_scid=fMUkW-RZoFCZuJhVYyyrzDOz6ServzlvpmxsDF0qBfteZlnuABrf.xjb-8-qAzQba43d; __tasessionId=o0i0eh7fx1586399591359"
    }
    params = {
        "category": "news_tech",
        "utm_source": "toutiao",
        "widen": "1",
        "max_behot_time": "0",
        "max_behot_time_tmp": "0",
        "tadrequire": "true",
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
