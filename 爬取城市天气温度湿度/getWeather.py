#-*-conding:utf-8-*-
import requests
import execjs

from json import loads
# from pymongo import MongoClient

# mongodb配置路径
MONGO_URL = 'mongodb://username:password@localhost:port'
MONGO_DB = 'weather'
MONGO_COLLECTION = 'temperature'

# 反混淆后的js文件
File = './weather.js'

class GetWeather(object):
    def __init__(self, method, city, time_type, start_time, end_time):
        '''
        :param method: 指定参数 GETCITYWEATHER
        :param city:  城市 上海/北京/成都
        :param time_type: 时间类型 HOUR/DAY
        :param start_time: 开始时间 2018-07-21 00:00:00
        :param end_time: 结束时间 2018-07-22 00:00:00
        '''
        self.method = method
        self.city = city
        self.time_type = time_type
        self.start_time = start_time
        self.end_time = end_time
        self.file = File

    # 获取解密后的接口数据
    def get_data(self):
        # 需要安装node.js
        node = execjs.get()
        ctx = node.compile(open(self.file).read())
        js = 'getData("{0}", "{1}", "{2}", "{3}", "{4}")'.format\
            (self.method, self.city, self.time_type, self.start_time, self.end_time)
        params = ctx.eval(js)
        api = 'https://www.aqistudy.cn/apinew/aqistudyapi.php'
        response = requests.post(api, data={'d': params})
        js = 'decodeData("{0}")'.format(response.text)
        data = loads(ctx.eval(js))['result']['data']['rows'] # 解析json数据
        return data

    # 存入mongodb
    def save_to_mongodb(self):
        items = self.get_data()
        conn = MongoClient(MONGO_URL)
        db = conn[MONGO_DB]
        collection = db[MONGO_COLLECTION]
        for item in items:
            data = {
                'city': self.city,
                'time': item['time'],
                'temperature': item['temp']
            }
            collection.insert_one(data)

def main():
    Weather = GetWeather('GETCITYWEATHER', '上海', 'HOUR', '2018-07-21 00:00:00', '2018-07-22 00:00:00')
    data = Weather.get_data()
    print(data)
    # Weather.save_to_mongodb()

    
if __name__ == '__main__':
    main()




