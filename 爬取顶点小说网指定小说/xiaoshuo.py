import requests
import re
import time
from lxml import etree

# //*[@id="list"]/dl/dd[1990]/a

# headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#                'Accept-Encoding':'gzip, deflate, br',
#                'Accept-Language':'zh-CN,zh;q=0.9',
#                'cookie':'PHPSESSID=u76v6sir759pqa2jh5o4m23d45; fikker-UIWD-APsN=wTN0ET9peOe6GBNFcvilmOiNWfyHCIJl; fikker-UIWD-APsN=wTN0ET9peOe6GBNFcvilmOiNWfyHCIJl; bookid=74240; bgcolor=; font=; size=; fontcolor=; width=; Hm_lvt_ebbbcda55dbd6bab51afaaf3f836a4da=1532880558,1532880706; chapterid=23729442; chaptername=%25u7B2C1982%25u7AE0%2520%25u767D%25u5C0F%25u6668%25u6765%25u4E86%25uFF08%25u4E8C%25uFF09; Hm_lpvt_ebbbcda55dbd6bab51afaaf3f836a4da=1532882383',
#                'Connection':'Keep-alive',
#                'Cache-Control':'max-age=0',
#                'Host':'www.23wxw.cc',
#                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5702.400 QQBrowser/10.2.1893.400'}
#
r = requests.Session()
html = r.get('https://www.23wxw.cc/html/74240/')
# print(html.text)

selector = etree.HTML(html.text)

base_url = 'https://www.23wxw.cc'

url_list = []

for i in range(2170, 2335):
    pipei = '//*[@id="list"]/dl/dd[{0}]/a/@href'.format(i)
    a = selector.xpath(pipei)[0]
    url = base_url + a
    url_list.append(url)
# print(url_list)

# url_list = ['https://www.23wxw.cc/html/74240/23538235.html']

for x in url_list:

    resp = r.get(x)
    selector = etree.HTML(resp.text)
    title = selector.xpath('//*[@id="wrapper"]/div[6]/div[2]/div[2]/h1/text()')[0]

    print('正在下载%s' %title)
    content = selector.xpath('//*[@id="content"]//text()')
    mystr = title + '\n'
    # time.sleep(5) 不是封Ip 而是检测是否带了cookie
    for q in content[0:-3]:
        w = re.sub(r'\r|\n|\t|\xa0', '', q)
        w += '\n'
        mystr += w
    with open('yhqx.txt', 'a+', encoding='utf-8') as f:
        f.write(mystr)




