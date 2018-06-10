import json
import re
from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup

def get_one_page(url):
    # 设置user-agent为浏览器 防止被反爬虫发现后禁止登陆
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3423.2 Safari/537.36'
    }
    # 获取网页 'http://maoyan.com/board/4'
    r = requests.get(url, headers=headers)
    # print(r.text)
    # 网页成功访问则返回页面内容 不成功返回空
    if r.status_code == 200:
        return r.text
    return None


def parse_one_page(html):
    soup = BeautifulSoup(html, 'lxml')
    pages = soup.select('.board-wrapper dd')
    # index = []
    # image = []
    # title = []
    # actor = []
    # time = []
    # score = []
    mylist = []
    for page in pages:
        # 排名
        for i in page.select_one('i'):
            if i.string:
                mylist.append(i.string)
        # 标题
        for i in page.select('.name a'):
            if i['title']:
                mylist.append(i['title'])

        # 图片地址
        # 动态加载 暂时不保存
        # for i in page.select('board-img'):
        #     if i:
        #         image.append(i)
        # 主演
        for i in page.select('.star'):
            if i.string:
                mylist.append(i.string.strip())
        # 上映时间
        for i in page.select('.releasetime'):
            if i.string:
                mylist.append(i.string)
        f = ''
        # 评分
        for i in page.select('.score'):
            for x in i.select('i'):
                for string in x:
                    f += string
            mylist.append(f)

    # 列表换字典
    c = 0
    all_list = ['index', 'title', 'actor', 'time', 'score']
    all_mylist = []
    for x in mylist:
        c += 1
        all_mylist.append(x)
        if c == 5:
            c = 0
            yield dict(zip(all_list, all_mylist))
            all_mylist = []


# 写入记事本中
def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def main():
    # 分页爬取 通过观察发现offset为每10换页
    for i in range(10):
        num = i * 10
        base_url = 'http://maoyan.com/board/4?'
        params = {'offset': num}
        # urlencode 拼接网址
        full_url = base_url + urlencode(params)
        html = get_one_page(full_url)
        # 返回为yield对象
        content = parse_one_page(html)
        # 写入result.txt
        for x in content:
            write_to_file(x)



if __name__ == '__main__':
    main()
