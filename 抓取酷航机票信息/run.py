import requests
import re

from lxml import etree

headers = {
    # 2018/08/13 cookie只有十分钟
    # "cookie": "DG_IID=F140DA92-ABA9-3687-BC52-7A18202A6783; DG_UID=DBEAF818-97E0-3D69-B8D3-2E3F05230B03; DG_SID=222.178.116.97:rr5JHTIRySavp3Nyr5giCA9jG3NvIB6vdm3Kxoim6lM; rxVisitor=1533869900156VLH8PAB0JVKIQA6CHOESSEIKO1E20HFS; CS_FPC=CSCwrhLtp485CW239OLkjkCnOH8LODBUOQD; _ga=GA1.3.164076498.1533869915; jumpseat_uid=XzK0_VPR1-hZQGZKVKhjhD; cookieconsent_status=dismiss; hpu=/zh; loc=CN; country=CN; optimizelyEndUserId=oeu1533870732535r0.509727876242688; optimizelySegments=%7B%222335550040%22%3A%22gc%22%2C%222344180004%22%3A%22campaign%22%2C%222354350067%22%3A%22false%22%2C%222355380121%22%3A%22cn-ao%22%7D; optimizelyBuckets=%7B%7D; _ga=GA1.2.748369651.1533870742; _gid=GA1.2.87653701.1534121037; ASP.NET_SessionId=k4ifhj24auuedoh2ktaxmn3m; dotrez=2534532106.20480.0000; _gid=GA1.3.87653701.1534121037; Hm_lvt_c2b8e393697aacf76c5b1874762308ea=1533870731,1534121032,1534121435; _gcl_dc=GCL.1534123303.CKjr5JPm6NwCFQ3jvAodSwcPBw; Hm_lpvt_c2b8e393697aacf76c5b1874762308ea=1534123350; acw_tc=AQAAADB72jBL1wAAYXSy3p9fkxYzTA1l; dtLatC=2; DG_ZID=5354ECD2-D55F-3CD4-B428-E496C2C2728A; DG_ZUID=753318BE-DB2D-3B33-9231-7042B1F41F4C; DG_HID=79B197A8-5F38-3A67-B7CF-57D34ADDD24E; dtPC=5$534502483_667h-vDDKGMKBKGIINKJMNMFAPPEGMNAHNBNHN; rxvt=1534138145987|1534136345987; dtCookie=5$2692EA7A2E1BE8AF843AD035B768296F|makeabooking.flyscoot.com|1; dtSa=true%7CS%7C-1%7CPage%3A%20%3Fculture%3Dzh-CN%7C-%7C1534137614723%7C534502483_667%7Chttps%3A%2F%2Fmakeabooking.flyscoot.com%2F%3Fculture%3Dzh-CN%7CSearch%7C1534134545965%7C",
    # 2018/08/13 15:05 --15:14
    # "cookie": "😒😒😒😒😒😒😒😒😒😒😒😒😒😒😒😒😒😒😒",
    "cookie": "DG_IID=F140DA92-ABA9-3687-BC52-7A18202A6783; DG_UID=DBEAF818-97E0-3D69-B8D3-2E3F05230B03; DG_SID=222.178.116.97:rr5JHTIRySavp3Nyr5giCA9jG3NvIB6vdm3Kxoim6lM; rxVisitor=1533869900156VLH8PAB0JVKIQA6CHOESSEIKO1E20HFS; CS_FPC=CSCwrhLtp485CW239OLkjkCnOH8LODBUOQD; _ga=GA1.3.164076498.1533869915; jumpseat_uid=XzK0_VPR1-hZQGZKVKhjhD; cookieconsent_status=dismiss; hpu=/zh; loc=CN; country=CN; optimizelyEndUserId=oeu1533870732535r0.509727876242688; optimizelyBuckets=%7B%7D; _ga=GA1.2.748369651.1533870742; _gid=GA1.2.87653701.1534121037; _gid=GA1.3.87653701.1534121037; tzmememberportal=9SJI63+ruQfp9o2e6aBTFzbZ9jNk8+H+juhzlRN40gI=; _gcl_dc=GCL.1534143862.CKjr5JPm6NwCFQ3jvAodSwcPBw; optimizelySegments=%7B%222335550040%22%3A%22gc%22%2C%222344180004%22%3A%22referral%22%2C%222354350067%22%3A%22false%22%2C%222355380121%22%3A%22cn-ao%22%7D; dotrez=2551309322.20480.0000; acw_tc=AQAAAF6XWzcg1QsAYXSy3m7kryCqoeUJ; ASP.NET_SessionId=5y4lcu1q50zblwg13f2zr3yw; Hm_lvt_c2b8e393697aacf76c5b1874762308ea=1534121435,1534138414,1534139379,1534152459; Hm_lpvt_c2b8e393697aacf76c5b1874762308ea=1534152479; startTime=MjAxOC0wOC0xMyAxNzo0MToxOQ==; dtLatC=1; DG_ZID=74137E08-8639-35B7-B9D5-C9469EEF7BF0; DG_ZUID=8BA3A430-E0F4-302F-B929-5DD4A68E2DF1; DG_HID=73D3CF53-B775-3D8E-BDA3-0913CC5F8A21; dtPC=5$554312202_34h-vFLFNNHMNAPPBOJBOCKLGJHNKFPBIOHAH; rxvt=1534156166106|1534152117762; dtCookie=5$4F69D2FD1884684E6CF486BE070EE312|makeabooking.flyscoot.com|1; dtSa=true%7CU%7C-1%7CManage%20My%20Booking%7C-%7C1534154896482%7C552549435_283%7Chttps%3A%2F%2Fmakeabooking.flyscoot.com%2Fmanage%3F_5Fga%3D2.192253795.87653701.1534121037-748369651.1533870742%7CManage%20Your%20Booking%20Online%20%5Ep%20Scoot%7C1534152584669%7C",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5221.400 QQBrowser/10.0.1125.400",
    # "referer": "https://makeabooking.flyscoot.com/?culture=zh-CN",
    # "referer": "https://www.flyscoot.com/zh?utm_source=baidu&utm_medium=search&utm_campaign=cn-ao&gclid=CKjr5JPm6NwCFQ3jvAodSwcPBw&gclsrc=ds&dclid=CKvC85Pm6NwCFdGWvQodiN0HlA",

}

data = {
    "revAvailabilitySearch.SearchInfo.Direction": "return",
    "revAvailabilitySearch.SearchInfo.SearchStations[0].DepartureStationCode": "ADL",
    "revAvailabilitySearch.SearchInfo.SearchStations[0].ArrivalStationCode": "SIN",
    "revAvailabilitySearch.SearchInfo.SearchStations[0].DepartureDate": "11/03/2018",
    "revAvailabilitySearch.SearchInfo.SearchStations[1].DepartureDate": "10/03/2018",
    "revAvailabilitySearch.SearchInfo.AdultCount": "1",
    "revAvailabilitySearch.SearchInfo.ChildrenCount": "0",
    "revAvailabilitySearch.SearchInfo.InfantCount": "0"
}

r = requests.Session()

r.headers = headers

# r.get('https://www.flyscoot.com/zh')

a = r.post("https://makeabooking.flyscoot.com/", data=data)

# cookie = a.cookies
#
# r.cookies = cookie

cookie = a.cookies.get_dict()
print(cookie)
print(cookie.get('acw_tc'))
print(type(cookie))

s = r.get("https://makeabooking.flyscoot.com/Book/Flight")

print(s.text)

selector = etree.HTML(s.text)

mylist1 = selector.xpath('//*[@id="departure-results"]/div') # 出发机票

mylist2 =  selector.xpath('//*[@id="return-results"]/div') # 返回机票

mylist = list(mylist1) + list(mylist2) # 合并

if not mylist:
    w = selector.xpath('//*[@id="dCF_captcha_text"]//text()')
    if w:
        find_url = re.findall(r'[a-zA-z]+://[^\s]*', w[0])[0]
        print(find_url)
    else:
        error = selector.xpath('//*[@class="server_error"]/h1/text()')
        if error:
            print('666')
list1 = []

for i in mylist:
    start_time = i.xpath('div[@class="flight__from"]/ul/li[1]/text()')[0] # CAN 10:45 拆分
    start_day = i.xpath('div[@class="flight__from"]/ul/li[3]/text()')[0] # Oct 30 (Tue) 拆分
    # 进行拼接
    a = start_time.split(' ')
    depTime = a[1] + ' ' + start_day # 出发时间
    depAirport = a[0] # 出发地点

    # start_place = i.xpath('div[@class="flight__from"]/ul/li[2]/text()')[0] # Guangzhou
    place_name = i.xpath('div[@class="flight__from"]/ul/li[last()]/img/@alt') # 飞机名称

    if not place_name:
        place_name = ""
    else:
        place_name = place_name[0]

    # 航班班次
    c = i.xpath('div[@class="flight__stop"]/div/@data-content')[0] # TR 404
    d = re.search(r'\:(.*?)\(', c).group(0)
    carrier = re.findall(r'[a-zA-Z]+', d)[0] # 航空公司代码
    carrier_num =  re.findall(r'\d+', d)[0] # 航班号数字
    flightNumber = carrier + carrier_num # 航班号(字母 + 数字)

    end_time = i.xpath('div[@class="flight__to"]/ul/li[1]/text()')[0] # SIN 15:00
    end_day = i.xpath('div[@class="flight__to"]/ul/li[3]/text()')[0] # Oct 30 (Tue)
    # 进行拼接
    b = end_time.split(' ')
    arrTime = b[1] + ' ' + end_day # 到达时间
    arrAirport = b[0] # 到达地点

    # end_place = i.xpath('div[@class="flight__to"]/ul/li[2]/text()')[0] # Singapore
    prices = i.xpath('div[@class="flight__fly"]/div[@class="fare-wrapper"]/button/span/text()')[0] # CNY540
    print(prices)

    currency = re.findall(r'[a-zA-Z]+', prices)[0]  # 货币种类

    price = re.sub(r'[a-zA-Z,]', '', prices) # 价格

    currency = re.findall(r'[a-zA-Z]+', prices)[0] # 货币种类


    mydict = {
        "carrier": carrier,
        "flightNumber": flightNumber,
        "depAirport": depAirport,
        "depTime": depTime,
        "arrAirport": arrAirport,
        "arrTime": arrTime,
        "price": price,
        "currency": currency
    }

    list1.append(mydict)

print(list1)









