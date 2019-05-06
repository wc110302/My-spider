import json


def get_header(headers):
    hs = headers.split('\n')
    b = [k for k in hs if len(k)]
    e = b
    f = {(i.split(":")[0], i.split(":", 1)[1].strip()) for i in e}
    g = sorted(f)
    header = "{\n"
    for k, v in g:
        header += repr(k).replace('\'', '"') + ': ' + repr(v).replace('\'', '"') + ',\n'
    header += "}"
    return json.loads(header.replace(',\n}', '\n}'))

headers = """
Accept: */*
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
Connection: keep-alive
Content-Length: 1347
Content-Type: application/x-www-form-urlencoded
Host: recommend.browser.qq.com
Origin: https://feeds.qq.com
Referer: https://feeds.qq.com/newtab/?adtag=newtab
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3676.400 QQBrowser/10.4.3469.400
"""

a = get_header(headers)
print(a)
print(type(a))