import json
import requests

from urllib.parse import urlencode
from pymongo import MongoClient

def get_one_page(url):
    # 设置user-agent为浏览器 防止被反爬虫发现后禁止登陆
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3423.2 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    return response.json()


def parse_dect(html):
    if html:
        items = html.get('data')
        for item in items:
            jiepai = {}
            jiepai['title'] = item.get('title')
            jiepai['datetime'] = item.get('datetime')
            jiepai['imgurl'] = item.get('image_list')
            yield jiepai


def save_to_mongodb(result):
    # 保存数据到mongodb
    conn = MongoClient('mongodb://1.1.1.1:27017')
    db = conn.jiepai
    connect = db['img']
    connect.insert(result)


def save_img_to_computer(items):
    # for item in items:
    #     for i in item['imgurl']:
    #         file_path = '{0}/{1}.{2}'.format(item['title'], i['url'].spilt('/')[-1], 'jpg')
    #         response = requests.get(i['url'])
    #         with open(file_path, 'wb') as f:
    #             f.write(response.content)
    for item in items:
        # 将截取的图片保存jpg格式
        if item['url']:
            file_path = '{0}.{1}'.format(item['url'].split('/')[-1], 'jpg')
            # 拼接图片的url
            url = 'http:' + item['url']
            response = requests.get(url)
            with open(file_path, 'wb') as f:
                f.write(response.content)


def main():
    # 头条url: https://www.toutiao.com/search/?keyword=街拍
    # 接口url: https://www.toutiao.com/search_content/?offset=40&format=json&keyword=%E8%A1%97%E6%8B%8D&autoload=true&count=20&cur_tab=1&from=search_tab
    base_url = 'https://www.toutiao.com/search_content/?'
    for i in range(1, 11):
        i *= 20
        prams = {
            'offset': i,
            'format': 'json',
            'keyword': '街拍', #街拍
            'autoload': 'true',
            'count': '20',
            'cur_tab': '1',
            'from': 'search_tab',
        }
        # 拼接url
        full_url = base_url + urlencode(prams)
        html = get_one_page(full_url) # 获取接口传输的json数据
        results = parse_dect(html) # 解析json数据保存到jiepai字典中
        # 遍历API传过来的json数据
        for result in results:
            print(result)
            # save_to_mongodb(result) # 保存数据到mongodb
            # save_img_to_computer(result['imgurl']) # 保存图片到本地


if __name__ == '__main__':
    main()