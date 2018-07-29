import re
import requests
import execjs
import urllib
from json import loads


File = '.my.js'

# cookie 开发者工具中获取 必须带上 否则报错
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
    'Cookie': 'BAIDUID=761A155CABDEEA77604C91E936B5692E:FG=1; BIDUPSID=761A155CABDEEA77604C91E936B5692E; PSTM=1532661805; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; H_PS_PSSID=1425_25809_21085; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1532773520; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1532773520; to_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; from_lang_often=%5B%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D; PSINO=3; locale=zh'
}

html = requests.get('http://fanyi.baidu.com', headers=headers)
html.encoding = 'utf-8'

# 正则匹配 gtk
matches = re.findall("window.gtk = '(.*?)';", html.text, re.S)
for match in matches:
    gtk = match

if gtk == "":
    print('Get gtk fail.')
    exit()

print('gtk = ' + gtk)

# 正则匹配 token
matches = re.findall("token: '(.*?)'", html.text, re.S)
for match in matches:
    token = match

if token == "":
    print('Get token fail.')
    exit()

print('token = ' + token)

# 从网页源代码中找出加密的js代码 解压缩处理
signCode = 'function a(r,o){for(var t=0;t<o.length-2;t+=3){var a=o.charAt(t+2);a=a>="a"?a.charCodeAt(0)-87:Number(a),a="+"===o.charAt(t+1)?r>>>a:r<<a,r="+"===o.charAt(t)?r+a&4294967295:r^a}return r}var C=null;var hash=function(r,_gtk){var o=r.length;o>30&&(r=""+r.substr(0,10)+r.substr(Math.floor(o/2)-5,10)+r.substr(-10,10));var t=void 0,t=null!==C?C:(C=_gtk||"")||"";for(var e=t.split("."),h=Number(e[0])||0,i=Number(e[1])||0,d=[],f=0,g=0;g<r.length;g++){var m=r.charCodeAt(g);128>m?d[f++]=m:(2048>m?d[f++]=m>>6|192:(55296===(64512&m)&&g+1<r.length&&56320===(64512&r.charCodeAt(g+1))?(m=65536+((1023&m)<<10)+(1023&r.charCodeAt(++g)),d[f++]=m>>18|240,d[f++]=m>>12&63|128):d[f++]=m>>12|224,d[f++]=m>>6&63|128),d[f++]=63&m|128)}for(var S=h,u="+-a^+6",l="+-3^+b+-f",s=0;s<d.length;s++)S+=d[s],S=a(S,u);return S=a(S,l),S^=i,0>S&&(S=(2147483647&S)+2147483648),S%=1e6,S.toString()+"."+(S^h)}'

source = '你是猪'
sign = execjs.compile(signCode).call('hash', source, gtk)
print('source = ' + source + ', sign = ' + sign)

# 请求接口
fromLanguage = 'zh'
toLanguage = 'en'

# API接口 不能使用post接口 否则报错
v2transapi = 'http://fanyi.baidu.com/v2transapi?from=%s&to=%s&query=%s' \
             '&transtype=translang&simple_means_flag=3&sign=%s&token=%s' % (fromLanguage, toLanguage, urllib.parse.quote(source), sign, token)
print(v2transapi)

translate_result = requests.get(v2transapi, headers=headers)
# 处理json数据 获取翻译单词
word = loads(translate_result.text)['trans_result']['data'][0]['dst']
print(word)
