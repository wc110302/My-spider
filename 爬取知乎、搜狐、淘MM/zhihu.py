import pymysql
from bs4 import BeautifulSoup
import re
from urllib.request import urlopen
import json
from datetime import datetime


def main():
    html = urlopen('https://www.zhihu.com/explore').read().decode('utf-8')
    bs = BeautifulSoup(html, 'lxml')
    # 获取www.zhihu.com/explore 页面下的推送文章
    htmls = bs.select('a[class="question_link"]')

    create_time = datetime.now()
    # 遍历
    for elem in htmls:
        # 创建数据库连接
        conn = pymysql.connect(host='47.106.122.64', user='root', password='123456', database='crawler', port=3306,
                               charset='utf8')
        # title = re.compile(r'>(.*)</a>')
        # title_list = re.findall(title, str(elem))
        # print(title_list)
        # 爬取网页的url
        link = elem.attrs['href']
        link = 'https://www.zhihu.com' + link
        # print(link)
        # 爬取每个网页里面的优选答案的内容
        html = urlopen(link).read().decode('utf-8')
        bs = BeautifulSoup(html, 'lxml')
        # 爬取单独网页里面的标题
        title = bs.select_one('.QuestionHeader-title')
        title1 = re.compile(r'>(.*)</h1>')
        title_list = str(re.findall(title1, str(title)))
        # 获取答案里面的每一行内容
        html_list = bs.select('.CopyrightRichText-richText p')
        # 定义一个空字符串用来存答案内容
        bs_sub = ''
        for myhtml in html_list:
            bs_sub += myhtml.text
        bs_sub = '最佳答案:' + bs_sub
        try:
            with conn.cursor() as cursor:
                cursor.execute('insert into tb_zhihu(ztitle, zanswer, create_time) values (%s, %s, %s)',
                               (title_list, bs_sub, create_time))
            conn.commit()
        finally:
             conn.close()

    print('上传成功')










if __name__ == '__main__':
    main()