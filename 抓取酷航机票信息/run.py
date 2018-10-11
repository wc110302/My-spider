import requests
import re

from lxml import etree

tt = 0
for _ in range(100):
    headers = {
        # 2018/08/13 cookie只有十分钟
        # "cookie": "DG_IID=F140DA92-ABA9-3687-BC52-7A18202A6783; DG_UID=DBEAF818-97E0-3D69-B8D3-2E3F05230B03; DG_SID=222.178.116.97:rr5JHTIRySavp3Nyr5giCA9jG3NvIB6vdm3Kxoim6lM; rxVisitor=1533869900156VLH8PAB0JVKIQA6CHOESSEIKO1E20HFS; CS_FPC=CSCwrhLtp485CW239OLkjkCnOH8LODBUOQD; _ga=GA1.3.164076498.1533869915; jumpseat_uid=XzK0_VPR1-hZQGZKVKhjhD; cookieconsent_status=dismiss; hpu=/zh; loc=CN; country=CN; optimizelyEndUserId=oeu1533870732535r0.509727876242688; optimizelySegments=%7B%222335550040%22%3A%22gc%22%2C%222344180004%22%3A%22campaign%22%2C%222354350067%22%3A%22false%22%2C%222355380121%22%3A%22cn-ao%22%7D; optimizelyBuckets=%7B%7D; _ga=GA1.2.748369651.1533870742; _gid=GA1.2.87653701.1534121037; ASP.NET_SessionId=k4ifhj24auuedoh2ktaxmn3m; dotrez=2534532106.20480.0000; _gid=GA1.3.87653701.1534121037; Hm_lvt_c2b8e393697aacf76c5b1874762308ea=1533870731,1534121032,1534121435; _gcl_dc=GCL.1534123303.CKjr5JPm6NwCFQ3jvAodSwcPBw; Hm_lpvt_c2b8e393697aacf76c5b1874762308ea=1534123350; acw_tc=AQAAADB72jBL1wAAYXSy3p9fkxYzTA1l; dtLatC=2; DG_ZID=5354ECD2-D55F-3CD4-B428-E496C2C2728A; DG_ZUID=753318BE-DB2D-3B33-9231-7042B1F41F4C; DG_HID=79B197A8-5F38-3A67-B7CF-57D34ADDD24E; dtPC=5$534502483_667h-vDDKGMKBKGIINKJMNMFAPPEGMNAHNBNHN; rxvt=1534138145987|1534136345987; dtCookie=5$2692EA7A2E1BE8AF843AD035B768296F|makeabooking.flyscoot.com|1; dtSa=true%7CS%7C-1%7CPage%3A%20%3Fculture%3Dzh-CN%7C-%7C1534137614723%7C534502483_667%7Chttps%3A%2F%2Fmakeabooking.flyscoot.com%2F%3Fculture%3Dzh-CN%7CSearch%7C1534134545965%7C",
        # 2018/08/13 15:05 --15:14
        # "cookie": "😒😒😒😒😒😒😒😒😒😒😒😒😒😒😒😒😒😒😒",
        "cookie": "acw_tc=0bc19b0515380296260735464e19f9050eed0a8d82ed5640eb12832aba8399; dotrez=3138577418.20480.0000; DG_SID=60.249.38.63:OjPn7KXhYfIuuKxwLfxNUpCTob6a9tWiOATxA2GhtWI; DG_IID=F66951DF-92E7-30AD-B54A-AC0C19896C30; DG_UID=9074038B-BBA2-3D13-8609-695001E3AED1; DG_ZID=27779CE6-79BE-3267-B1CC-C20685319528; DG_ZUID=9D571060-7746-3603-BA45-686F132583EB; DG_HID=B40613AC-FE22-36AD-9B6E-D0DB2D9C9570; ASP.NET_SessionId=rfbn11vhlytsqvglpe12zblo; startTime=MjAxOC0wOS0yNyAxNDoyNzoyOQ==; CS_FPC=CSCg4vm3o4nSpUOaXCdkAVrtL2p6I10tFxD; _gcl_au=1.1.1056609755.1538029650; _ga=GA1.3.1672102088.1538029660; _gid=GA1.3.1720611526.1538029660; dtPC=5$229648270_783h-vFDPSJFEHPLIJDKANVJDBJNIDBIAOKIJM; rxVisitor=1538029648275G87DHG97F8ODGPI5I5IJR2IV9S4GLBE2; rxvt=1538031628684|1538027245597; dtLatC=280; dtCookie=5$707C467CCCA8E7BDEDA96EDE6C16E6DD|makeabooking.flyscoot.com|1; dtSa=true%7CU%7C-1%7C1%E8%88%AA%E7%8F%AD%202%E4%B9%98%E5%AE%A2%E4%BF%A1%E6%81%AF%203%E5%BA%A7%E4%BD%8D%204ADD-ONS%205%E4%BB%98%E6%AC%BE%E9%80%89%E6%8B%A9%E8%88%AA%E7%8F%AD%7C-%7C1538029856614%7C229648270_783%7Chttps%3A%2F%2Fmakeabooking.flyscoot.com%2Fbook%2FFlight%2FSelect%3Fculture%3Dzh-CN%26type%3D1%26dst1%3DCAN%26ast1%3DSIN%26dd%3D2018-10-05%26adt%3D1%26chd%3D0%26inf%3D0%7C%E9%80%89%E6%8B%A9%E8%88%AA%E7%8F%AD%7C1538029828684%7C",
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
    r.verify = False

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
    if list1:
        tt += 1
print(tt)











