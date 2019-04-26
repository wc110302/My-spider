import re
import json
import random

import csv
import requests
from lxml import etree


def parse_detail(data, city, company, ID, status):
    with open('lasCnasCompany{0}.csv'.format(city), 'a+', encoding='utf-8-sig', newline='') as csvfile1:
        for x in data:
            spamwriter2 = csv.writer(csvfile1, dialect=('excel'))
            # 设置标题
            if not status:
                spamwriter2.writerow(
                    ["公司名", "注册编号", "检测对象", "序号", "名称", "检测标准（方法）", "说明", "状态"])
                status = True
            thisObject = x.get('objCh')  # 检测对象
            thisNum = x.get('paramNum')  # 序号
            thisName = x.get('paramCh')  # 名称
            thisWay = x.get('stdAllDesc')  # 检测标准(方法)
            thisExplain = x.get('limitCh')  # 说明
            thisStatus = '有效'  # 状态
            spamwriter2.writerow(
                [company, ID, thisObject, thisNum, thisName, thisWay, thisExplain, thisStatus])


cities = ['上海', '北京']

for city in cities:
    page = 1
    for q in range(page):
        count = 0
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
        }

        s = requests.Session()

        r = s.get('https://las.cnas.org.cn/LAS/publish/externalQueryL1.jsp', headers=headers)
        print(r.text)

        r = s.get('https://las.cnas.org.cn/LAS/verify/getValidateCode.action?fleshCode={0}'.format(str(random.uniform(0, 1))), headers=headers)
        with open('verify.jpg', 'wb') as f:
            f.write(r.content)

        url = 'http://127.0.0.1:4006/verify' # 验证码识别接口

        data = open("verify.jpg", "rb").read()

        verify = requests.post(url, data=data).json().get('code')
        print(verify)

        data = {
            "verifyCode": verify
        }

        r = s.post('https://las.cnas.org.cn/LAS/verify/verifyCode.action?fleshCode={0}'.format(str(random.uniform(0, 1))), headers=headers, data=data)
        # print(r.text)

        data = {
            "labType": "L",
            "choType": "L",
            "orgState": "0",
            "searchLang": "CH",
            "orgAddress": city,
            "orgAreaSel": "00",
            "authInterceptCode": verify,
            "startIndex": str(q * 100),
            "sizePerPage": "100",
        }

        r = s.post('https://las.cnas.org.cn/LAS/publish/queryPublishLicenseList.action?', headers=headers, data=data)
        # print(r.text)
        company = r.json().get('data')
        page = int(r.json().get('pageCount')) # 共计多少页
        print('共计{0}页'.format(page))
        with open('lasCnas{0}.csv'.format(city), 'a+', encoding='utf-8-sig', newline='') as csvfile:

            spamwriter = csv.writer(csvfile, dialect=('excel'))
            # 设置标题
            spamwriter.writerow(["公司名", "注册编号", "报告", "联系人", "联系电话", "邮政编码", "传真号码", "电子邮箱", "单位地址", "认可有效期", "暂停项目/参数", "网站地址", "认可能力范围"])

            for i in company:
                try:
                    companyName = i.get('orgName') # 公司名
                    url = "https://las.cnas.org.cn/LAS/publish/queryOrgInfo1.action?id={0}&orgEnOrCh=Ch&authInterceptCode={1}".format(i.get('uuid'), verify)
                    r = s.get(url, headers=headers)
                    # print(r.text)
                    selector = etree.HTML(r.text)
                    info = selector.xpath('//span[@class="clabel"]')
                    print(companyName)
                    print(info)
                    ID = ''.join(info[0].xpath('.//text()')).replace(' ', '').replace('\n', '').replace('\t', '') # 注册编号
                    report = ''.join(info[1].xpath('.//text()')) # 报告/证书允许使用认可标识的其他名称
                    contacts = ''.join(info[2].xpath('.//text()')) # 联系人
                    phone = ''.join(info[3].xpath('.//text()')) # 联系电话
                    postCode = ''.join(info[4].xpath('.//text()')) # 邮政编码
                    fax = ''.join(info[5].xpath('.//text()')) # 传真号码
                    web = ''.join(info[6].xpath('.//text()')) # 网站地址
                    email = ''.join(info[7].xpath('.//text()')) # 电子邮箱
                    address = ''.join(info[8].xpath('.//text()')) # 单位地址
                    validity = ''.join(info[9].xpath('.//text()')) + '-' + ''.join(info[10].xpath('.//text()')) # 认可有效期
                    product = ''.join(info[11].xpath('.//text()')) # 暂停项目/参数
                    # web = ''.join(selector.xpath('/html/body/div/table[1]/tbody/tr[5]/td[1]/span/a//text()')) # 网站地址
                    print(ID)
                    print(report)
                    print(contacts)
                    print(phone)
                    print(postCode)
                    print(fax)
                    print(email)
                    print(address)
                    print(validity)
                    print(product)
                    print(web)

                    a = re.findall("<a href=\"javascript:void\(0\)\"  onClick=\"_showdown\('(.*?)'\)", r.text)
                    if a:
                        nextUrl = "https://las.cnas.org.cn" + a[0]
                        # print(nextUrl)
                        r = s.get(nextUrl, headers=headers)
                        if "认可的检测能力范围" in r.text:
                            print('存在数据')
                            finalUrl = "https://las.cnas.org.cn"  + re.findall("contentsURL : '(.*?)'", r.text)[2]
                            print(finalUrl)
                            r = s.get(finalUrl, headers=headers)
                            # print(r.text)
                            branchId = re.findall('<option value="(.*?)">', r.text)[0]
                            effBranchIds = '{0}'.format(branchId)
                            baseinfoId = re.findall('baseInfoId=(.*?)&', finalUrl)[0]
                            data = {
                                "baseinfoId": baseinfoId,
                                "type": "L1",
                                "enstart": "0",
                                "branchId": branchId,
                                "effBranchIds": effBranchIds,
                                "startIndex": "0",
                                "sizePerPage": "100"
                            }
                            finalData = s.post('https://las.cnas.org.cn/LAS/publish/queryPublishLCheckObj.action?', headers=headers, data=data).json().get('data')
                            print(finalData)
                            print(len(finalData))
                            # for x in finalData:
                            parse_detail(finalData, city, companyName, ID, count)
                            count += 1
                        else:
                            finalData = '无'
                            print('不存在其他数据')
                    else:
                        finalData = '无'
                        print('不存在其他数据')

                    # 将CsvData中的数据循环写入到CsvFileName文件中

                    spamwriter.writerow([companyName, ID, report, contacts, phone, postCode, fax, email, address, validity, product, web, finalData])
                    print(1)
                    print(web)
                except Exception as e:
                    print(e)
                    continue
