# encoding:utf-8
import requests
from bs4 import BeautifulSoup
import re
import json
import os
from urllib.request import urlopen

# url='https://wenku.baidu.com/view/0571dbdf6f1aff00bed51e62.html?sxts=1539958717044'
jsList = []
picList = []
if not os.path.exists('./img/'):
    os.makedirs('./img/')


def parserJS(num):  # 文章地址
    global add, docType
    file = open("./urls/{}.txt".format(num))
    urls = []
    while 1:
        lines = file.readlines(100000)
        if not lines:
            break
        for line in lines:
            print(line)  # do something
            urls.append(line.replace('\n', ''))
    file.close()
    for url in urls:
        r = urlopen(url)
        soup = BeautifulSoup(r.read().decode('gb18030'), 'html.parser')
        script = soup.find_all('script', attrs={'type': 'text/javascript'})
        for i in script:
            if 'WkInfo.htmlUrls' in i.text:
                # print(i.text)
                add = i.text
            if 'WkInfo.Urls' in i.text:
                Doc = i.text
                # print(Doc)
            # print(i.text)

        # print(Doc)
        DocInfo = Doc.split('WkInfo.DocInfo=')[0]

        # print(DocInfo)
        docType = re.findall(r'\'docType\': \'\w+\'', DocInfo)[0]
        # print(docType)
        docType = docType.split(':')[1].replace('\'', '').strip(' ')
        title = re.findall(r'\'title\': \'.*\'', DocInfo)[0]
        docId = re.findall(r'\'docId\': \'.*\'', DocInfo)[0]
        docId = docId.split(':')[1].replace('\'', '').strip(' ')
        title = title.split(':')[1].replace('\'', '').strip(' ')
        print(title)
        print('文档的类型为%s' % docType)

        if docType == 'doc' or docType == 'txt':
            parserDoc(add, title)
        if docType == 'ppt':
            parserPPt(docId, title)
        if docType == 'pdf':
            parserPDF(add, title)


def parserDoc(add, file_name):
    add = add.split(' WkInfo.htmlUrls =')[1].split(';')[0]
    add = add.replace('\\x22', '').replace('\\', '')
    add = re.findall(r'pageLoadUrl:.*\w', add)[0].split(',')
    # print(add)

    for j in add:
        if 'json' in j:
            jsList.append(j.split(':', 1)[1].replace('}', '').strip(']'))

    print('共有%d页' % len(jsList))
    for i in jsList:
        parserPage(i, file_name)


def parserPPt(docId, file_name):
    print('Downloading pictures······')
    # print(docId)
    r = urlopen('https://wenku.baidu.com/browse/getbcsurl?doc_id=%s&pn=1&rn=99999&type=ppt' % docId)
    print(r.url)
    result = r.json()
    print('共有%d页' % len(result))
    for i in result:
        r = urlopen(i['zoom'])
        # print(i['zoom'])
        print('Downloading page %d' % i['page'])
        with open('./img/' + file_name + '%d.jpg' % i['page'], 'wb') as fd:
            fd.write(r.read().decode('gb18030'))


def parserPDF(add, file_name):
    add = add.split(' WkInfo.htmlUrls =')[1].split(';')[0]
    add = add.replace('\\x22', '').replace('\\', '')
    add = re.findall(r'pageLoadUrl:.*\w', add)[0].split(',')
    # print(add)

    for j in add:
        if 'png' in j:
            picList.append(j.split(':', 1)[1].replace('}', '').strip(']'))
    picList.remove(picList[0])

    print('共有%d页' % len(picList))

    for i in range(len(picList)):
        r = urlopen(picList[i])
        with open('./img/data%d.png' % i, 'wb') as fd:
            fd.write(r.read())


def parserPage(url, file_name):  # js地址
    r = urlopen(url.replace('\\', ''))  # 访问js
    result = json.loads(r.read().decode('gb18030').split('(', 1)[1].strip(')'))  # 转为json格式
    body = result['body']
    for i in body:
        if i['t'] == 'word':
            text = i['c']
            # if type(text)!=str:
            #     continue
            if i['ps'] != None and '_enter' in i['ps'].keys():
                text = '\n'

            print(text, end='')
            with open('./txt/' + file_name + '.txt', 'a', encoding='utf-8') as fd:
                fd.write(text)


if __name__ == '__main__':
    # url = 'https://wenku.baidu.com/view/e022413d67ec102de2bd8983.html'
    # parserJS(url)
    pass
