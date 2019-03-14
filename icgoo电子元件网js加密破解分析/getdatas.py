import re

import requests
import execjs

import Proxys

headers = {
    "Host": "www.icgoo.net",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6821.400 QQBrowser/10.3.3040.400",
    "Upgrade-Insecure-Requests": "1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    # "Cookie": "Hm_lvt_b77c434112432087e7f2d39059529519=1552551537; Hm_lpvt_b77c434112432087e7f2d39059529519=1552551537; history=\"[u'AD620']\""
}

proxies = Proxys.get_proxy()
s = requests.Session()
r = s.get("https://www.icgoo.net/search/?partno=AD620&qty=1&tdsourcetag=s_pcqq_aiomsg", headers=headers, proxies=proxies)
# print(r.text)
try:
    token_ = re.findall("getToken\(sups\[i\], '(.*?)'\)", r.text)[0]
except Exception as e:
    print(e)
    print('无法捕捉token')

supps = 'mouser,digikey,rochester,element14,hot,chip1stop,oem,future,element14_sh,online,arrow,verical,heilind,rs_china,rs_hk,avnet,questcomp,other,peigenesis,rutronik,tme,allied,corestaff,overstock,peigenesis_cn,excess,arrow_special,distrelec,rs_pro,microchip,icgoo_must_buy_parts,buerklin,epc,runic'
supp_list = supps.split(',')
token_list = []

for i in range(len(supp_list)):
    _JS = execjs.compile(open("myjs.js", "r").read())  # 初始化JS
    token = _JS.call("getToken", supp_list[i], token_)
    token_list.append(token)
print(token_list)

token_list = token_list[:3] # 取前3个试水

headers2 = {
    "Host": "www.icgoo.net",
    "Connection": "keep-alive",
    "Accept": "*/*",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
    "Referer": "https://www.icgoo.net/search/?partno=AD620&qty=1&tdsourcetag=s_pcqq_aiomsg",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    # "Cookie": "Hm_lvt_b77c434112432087e7f2d39059529519=1552551537; Hm_lpvt_b77c434112432087e7f2d39059529519=1552551537; history=\"[u'AD620']\""
}
for i in range(len(token_list)):
    url = "https://www.icgoo.net/search/getdata/?sup={0}&partno=AD620&qty=1&token={1}".format(supp_list[i], token_list[i])
    print(url)
    r = s.get(url, headers=headers2, proxies=proxies)
    print(r.text)