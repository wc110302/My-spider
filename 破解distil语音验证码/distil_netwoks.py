from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import os


def yzm(driver):

    driver.switch_to.frame('fc-iframe-wrap')  # 切换到iframe 下标0  CaptchaFrame  fc-iframe-wrap

    driver.find_element_by_class_name('fc_meta_audio_btn').click()
    print('2')
    time.sleep(1)
    try:
        for _ in range(5): # 循环5次尝试识别语音验证码

            download_time = time.time()

            driver.find_element_by_id('audio_download').click()  # 下载数字语音

            driver2 = webdriver.Chrome()

            driver2.get('http://www.iflyrec.com/html/addMachineOrder.html') # 讯飞语音在线识别网址

            time.sleep(3) # 等待网页加载

            b = os.listdir('e:\\sound') # 扫描下载路径

            driver2.find_element_by_name('file').send_keys('E:\\sound\\{0}'.format(b[0])) # 上传文件

            time.sleep(10)  # 等待识别 若网络较慢 可以适当延长

            a = driver2.find_element_by_id('t_WU_FILE_0').text # 获取文本

            sound_text = str_clerar(a) # 处理文本

            driver2.quit() # 关闭讯飞语音识别

            driver.find_element_by_class_name('response_field').click()
            driver.find_element_by_class_name('response_field').send_keys(sound_text)

            driver.find_element_by_id('audio_submit').click() # 进行验证

            os.remove('e:\\sound\\{0}'.format(b[0]))  # 删除音频文件

            time.sleep(1)

            audio_error = driver.find_element_by_xpath('//*[@id="audio_error"]/p').text # 错误标签

            print(audio_error)

            if not audio_error: # 若无错误标签则验证通过 跳出循环
                break
        if a == 5:
            return 0

        return 1

    except:
            return 0

def is_yzm(driver, out_time=10):
    try:
        WebDriverWait(driver, out_time - 5).until(EC.presence_of_element_located((By.ID, 'distilCaptchaForm')))  # 判断是否加载 FunCAPTCHA
        time.sleep(2)
        yzm(driver) # 破解验证码进入下一步
        return 1
    except:
        return 0


# 处理讯飞语音识别后的文本 可根据语音情况进行修改
def str_clerar(mystr):
    mystr = re.sub('。|！|!', '', mystr)
    mystr = re.sub('零', '0', mystr)
    mystr = re.sub('一', '1', mystr)
    mystr = re.sub('二', '2', mystr)
    mystr = re.sub('三', '3', mystr)
    mystr = re.sub('四|是', '4', mystr)
    mystr = re.sub('五', '5', mystr)
    mystr = re.sub('六', '6', mystr)
    mystr = re.sub('七', '7', mystr)
    mystr = re.sub('八', '8', mystr)
    mystr = re.sub('九|酒', '9', mystr)
    return mystr


def main():

    myPath = 'e:\\sound\\' # 存储音频地址

    options = webdriver.ChromeOptions()
    prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': myPath}  # 设置下载路径 第一个参数为不弹框 第二个参数为配置路径
    options.add_experimental_option('prefs', prefs)
    # options.add_argument("--headless")

    driver = webdriver.Chrome(chrome_options=options)

    driver.get('your url of distil networks')

    is_yzm(driver)  # 识别验证码


if __name__ == '__main__':
    main()