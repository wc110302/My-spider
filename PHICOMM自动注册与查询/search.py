import requests
import re

from lxml import etree

username = 'username'
password = 'password'

s = requests.Session()

headers3 = {
    "Host": "mall.phicomm.com",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5221.400 QQBrowser/10.0.1125.400",
    "Upgrade-Insecure-Requests": "1",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
}

r = s.get('https://mall.phicomm.com/passport-post_login.html', headers=headers3)

# print(r.headers)
a = r.headers.get('Set-Cookie')
b = a.split(';')
cookie1 = b[0] + ";" + b[4] + ";"


# headers4 = {
#     "Host": "mall.phicomm.com",
#     "Connection": "keep-alive",
#     "Content-Length": "0",
#     "Accept": "*/*",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5221.400 QQBrowser/10.0.1125.400",
#     "Origin": "https://mall.phicomm.com",
#     "X-Requested-With": "XMLHttpRequest",
#     "Referer": "https://mall.phicomm.com/passport-post_login.html",
#     "Accept-Encoding": "gzip, deflate, br",
#     "Accept-Language": "zh-CN,zh;q=0.9",
#     "Cookie": cookie1
# }
#
# r = s.post('https://mall.phicomm.com/index.php/openapi/cart/count', headers=headers4)
# print(r.headers)
# a = r.headers.get('Set-Cookie')
# b = a.split(';')
# cookie2 = b[0]

headers = {
    "Host": "mall.phicomm.com",
    "Connection": "keep-alive",
    "Content-Length": "45",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Origin": "https://mall.phicomm.com",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5221.400 QQBrowser/10.0.1125.400",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Referer": "https://mall.phicomm.com/passport-login.html",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
}

data = {
    "forward": "",
    "uname": username,
    "password": password
}

r = s.post('https://mall.phicomm.com/passport-post_login.html', headers=headers, data=data)

a = r.headers.get('Set-Cookie')
b = a.split(';')

c = b[5].split(',')
d = b[6].split(',')

cookie2 = b[0] + ";" + b[4] + ";" + c[1] + ";" + d[1] + ";"


headers1 = {
    "Host": "mall.phicomm.com",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5221.400 QQBrowser/10.0.1125.400",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Referer": "https://mall.phicomm.com/passport-login.html",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cookie": cookie1 + cookie2
}

r = s.get('https://mall.phicomm.com', headers=headers1)

# print(r.text)
# print(r.headers)

a = r.headers.get('Set-Cookie')
b = a.split(';')

c = b[4]
c = re.sub(' ', '', c)
cookie3 = re.sub(',', '', c)


headers2 = {
    "Host": "mall.phicomm.com",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5221.400 QQBrowser/10.0.1125.400",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Referer": "https://mall.phicomm.com/my.html",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cookie": cookie1 + cookie2 + cookie3
}

r = s.get('https://mall.phicomm.com/my-vclist.html', headers=headers2)
html1 = r.text
selector = etree.HTML(html1)
# total = selector.xpath('//*div[@class="my-vc-num"]/span/text()')
try:
    total = selector.xpath('/html/body/div[2]/div/div/div[2]/div/div[2]/div/div[1]/p/span/text()')[0]
    viable = selector.xpath('/html/body/div[2]/div/div/div[2]/div/div[2]/div/div[2]/div[1]/p/text()')[0]
    status = selector.xpath('/html/body/div[2]/div/div/div[2]/div/div[3]/table/tbody/tr/td[4]/text()')[0]
    viable_time = selector.xpath('/html/body/div[2]/div/div/div[2]/div/div[3]/table/tbody/tr/td[5]/text()')[0]
    print('总余额为:{0}, 可用余额为{1}, 状态为:{2}, 预计解冻时间为:{3}'.format(total, viable.strip(), status.strip(), viable_time))

except:
    print('账户余额可能为空,请查证')

r = s.get('https://mall.phicomm.com/my-orders.html', headers=headers2)

html2 = r.text
selector2 = etree.HTML(html2)

mylist = selector2.xpath('//div[contains(@class, alert-info)]')

for i in mylist:
    a = i.xpath('h2/text()')
    if a:
        print('订单:{0}'.format(a))

mylist2 = selector2.xpath('//div[@class="my-orders-list"]/table[contains(@class, "order_goods")]')

for i in mylist2:
    order_name = i.xpath('tbody/tr/td[1]/div/div[2]/a/text()')
    order_time = i.xpath('thead/tr/th[1]/ul/li[2]/text()')
    order_status = i.xpath('thead/tr/th[3]/span/text()')
    try:
        print('商品名称:{0}, 商品下单时间:{1}, 商品状态:{2}'.format(order_name[0].strip(), order_time[0].strip(), order_status[0].strip()))
    except:
        pass


