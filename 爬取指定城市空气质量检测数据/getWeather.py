import pandas as pd
import time
import os
from selenium import webdriver

## 创建存放爬取的临时文件的文件夹
if not os.path.exists('result'):
    os.mkdir('result')

## 组装日期, return list (201501-201712)
year = 2015
yearMonthList = []
while year <= 2017:
    month = 1
    while month <= 12:
        monthStr = '0' + str(month) if month <= 9 else str(month)
        yearStr = str(year)
        yearMonthList.append(yearStr + monthStr)
        month += 1
    year += 1

# # 删除多余月份
# i = 0
# while i <= 10:
#     yearMonthList.pop(0)
#     if i <= 3:
#         yearMonthList.pop(-1)
#     i += 1

df = pd.read_excel('city.xlsx', header=0)
# city这台计算机需要处理的城市，因为使用selenium爬取速度很慢，所以分到4台机器上运行。
# 若要几台电脑同时运行：city = df[df['machine'] == 'pc1']['city']，下次考虑直接用远程数据库写分布式
city = df['city']

## 组装url ,return urlList
cityUrlDict = {}

for eachCity in city:
    cityUrlDict[eachCity] = {}
    for eachDate in yearMonthList:
        cityUrlDict[eachCity][eachDate] = 'https://www.aqistudy.cn/historydata/daydata.php?city={}&month={}'.format(eachCity, eachDate)

df = pd.DataFrame(cityUrlDict)

## 使用selenium模拟浏览器行为
# 加启动配置，令chrome后台运行
option = webdriver.ChromeOptions()
option.add_argument('headless')
browser = webdriver.Chrome(chrome_options=option)

# 打开任意首页并停留，之所以有多余的首页，是为了关闭标签时不完全退出浏览器。
browser.get('https://www.baidu.com/')
# 获得主页的句柄，便于后面切换。
homePage = browser.current_window_handle

# 这里如果太快了容易崩溃，可以用一个字段去标记、分发。
for i,eachCity in enumerate(city):
    # 打开新页面
    eachCityUrl = df.ix[:, eachCity]
    for j,url in enumerate(eachCityUrl):
        browser.switch_to.window(homePage)
        # 在界面中运行js，在新标签页中打开界面
        newUrl = 'window.open("{}")'.format(url)
        browser.execute_script(newUrl)
        browser.switch_to.window(browser.window_handles[-1])
        title = browser.title
        # 若发生错误，刷新后再重试一次，实际上不是个好方法。
        try:
            time.sleep(2)
            # 这个js是通过分析前端源码得出的，在console中调试过console.log(items)，实际上不需要这么复杂。
            result = browser.execute_script("return items")
            browser.close()
        except:
            browser.refresh()
            time.sleep(5)
            result = browser.execute_script("return items")
            browser.close()
        # 如果获得的items不为空
        if len(result) > 0:
            for each in result:
                each['city'] = eachCity
            df2 = pd.DataFrame(result)
            df2.to_csv('result//' + each['city'] + each['time_point'][0:7] + '.csv', index_label='index')
        else:
            l = ['empty_flag']
            df2 = pd.DataFrame(l)
            df2.to_csv('result//' + eachCity +  url[-6:-2]+'-'+url[-2:] +'_empty' + '.csv',
                      index_label='index')

        print("该城市进度{}/{}，城市序号{}/{}，当前页面标题：{}".format(j+1,len(eachCityUrl),i + 1, len(city),title))
browser.quit()
print('done，开始合并文件')

files = os.listdir('result')
l_clean = []
for each in files:
    if not 'empty' in each:
        l_clean.append(each)

for i,each in enumerate(l_clean):
    maxNum = len(l_clean)
    if i == 0:
        path = 'result/'+each
        f = open(path,'r',encoding='utf-8')
        df = pd.read_csv(f,index_col='index')
    else:
        path = 'result/'+each
        print(i+1, '/', maxNum,'----',each)
        f = open(path,'r',encoding='utf-8')
        df2 = pd.read_csv(f,index_col='index')
        df = df.append(df2)
df2 = df.sort_values(by=["city","time_point"], ascending=[True, True]).reset_index(drop=True)
df2.to_csv('weather.csv', index_label='index')
print('合并文件完成')
