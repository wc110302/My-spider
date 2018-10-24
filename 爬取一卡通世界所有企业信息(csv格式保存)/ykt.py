import requests
from lxml import etree
import csv

s = requests.Session()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
}
s.headers = headers

with open('Pyw.csv', 'w', encoding='utf-8-sig') as csvfile:

    spamwriter = csv.writer(csvfile, dialect=('excel'))
    # 设置标题
    spamwriter.writerow(["企业名", "代理商", "主营产品", "联系人", "地址", "电话", "手机", "网址"])
    for i in range(1, 277):
        r = s.get('http://company.yktworld.com/comapny_search.asp?page={0}&tdsourcetag=s_pcqq_aiomsg'.format(i))

        r.encoding = 'gb2312'

        print(r.text)

        selector1 = etree.HTML(r.text)

        list1 = selector1.xpath('/html/body/div[4]/div[1]/div[2]/div')

        for i in list1[2:-1]:
            name = i.xpath('b/a/text()')[0]
            url = i.xpath('b/a/@href')[0]
            agent = i.xpath('font/text()')[0]
            product = i.xpath('div/text()[1]')[0]
            r = s.get(url)
            r.encoding = 'gb2312'
            selector2 = etree.HTML(r.text)
            contacts = selector2.xpath('/html/body/div[4]/div[1]/div[6]/text()[2]')
            if contacts:
                contacts = contacts[0]
            else:
                contacts = ''
            address = selector2.xpath('/html/body/div[4]/div[1]/div[6]/text()[3]')
            if address:
                address = address[0]
            else:
                address = ''
            tel = selector2.xpath('/html/body/div[4]/div[1]/div[6]/text()[4]')
            if tel:
                tel = tel[0]
            else:
                tel = ''
            phone = selector2.xpath('/html/body/div[4]/div[1]/div[6]/text()[5]')
            url1 = '暂无'
            try:
                if phone[0]:
                    if phone[0].split('：')[0].strip() == '手机':
                        phone = phone[0]
                    elif phone[0].split('：')[0].strip() == '网址':
                        url1 = phone[0]
                    else:
                        phone = '暂无'
                else:
                    phone = '暂无'
            except:
                phone = '暂无'
            if url1 != "暂无":
                phone = '暂无'
            url2 = selector2.xpath('/html/body/div[4]/div[1]/div[6]/text()[6]')
            if url2:
                url2 = url2[0]
                if url2.split('：')[0].strip() == '网址':
                    url1 = url2
                else:
                    url2 = ''
            else:
                url2 = ''
            print(name, agent, product, contacts, address, tel, phone, url1)
            # 将CsvData中的数据循环写入到CsvFileName文件中
            spamwriter.writerow([name, agent, product, contacts, address, tel, phone, url1])