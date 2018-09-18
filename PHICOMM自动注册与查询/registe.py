from selenium import webdriver
from PIL import Image
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree
import time
import re
import os

from rk import RClient

phone = 'phone'
password = 'password'

print('此次注册的账号为 %s'%phone)
print('此次注册的密码为 %s'%password)

driver = webdriver.Chrome()

driver.maximize_window()


driver.get('https://k.phicomm.com/dist/#/register')

driver.save_screenshot('verify.png')
element = driver.find_element_by_id("verifyCanvas")
# print(element.location)
# print(element.size)
left = element.location['x']
top = element.location['y']
right = element.location['x'] + element.size['width']
bottom = element.location['y'] + element.size['height']

im = Image.open('verify.png')
im = im.crop((left, top, right, bottom))
im.save('verify.png')

# js = """
#     document.getElementsByClassName('inputGroup')[0].value='18883362563';
#     document.getElementsByClassName('inputGroup')[1].value='442891187';
#     document.getElementsByClassName('inputGroup')[2].value='442891187';
#     document.getElementById('checkbox').click()
# """
#
# driver.execute_script(js)

rc = RClient('username', 'password', 'soft_id', 'soft_key') # 从若快官网注册用户以及开发者即可接入
im = open('verify.png', 'rb').read()
verify = rc.rk_create(im, 3040).get('Result')
print(verify)

element = driver.find_elements_by_class_name('inputGroup')
element[0].send_keys(phone)
element[1].send_keys(password)
element[2].send_keys(password)
driver.find_element_by_id('checkbox').click()  # 接受协议

driver.find_element_by_id('code_input').send_keys(verify) # 输入图片验证码

driver.find_element_by_id('verifyphonebtn').click() # 获取手机验证码

print('请输入手机验证码！')

verify_phone = input()

element = driver.find_elements_by_class_name('code_input')
element[1].send_keys(verify_phone) # 输入手机验证码

driver.find_element_by_class_name('btn').click()  # 提交注册

# with open('K.txt', 'r') as f:
#     K_key = f.read()

################################################登陆分割线#####################################################
time.sleep(2) # 防止跳转过快

element = driver.find_elements_by_class_name('inputGroup')
element[0].send_keys(phone) # 账号
element[1].send_keys(password) # 密码

driver.save_screenshot('verify.png')
element = driver.find_element_by_id("verifyCanvas")
# print(element.location)
# print(element.size)
left = element.location['x']
top = element.location['y']
right = element.location['x'] + element.size['width']
bottom = element.location['y'] + element.size['height']

im = Image.open('verify1.png')
im = im.crop((left, top, right, bottom))
im.save('verify1.png')

rc = RClient('username', 'password', 'soft_id', 'soft_key') # 从若快官网注册用户以及开发者即可接入
im = open('verify1.png', 'rb').read()
verify1 = rc.rk_create(im, 3040).get('Result')

driver.find_element_by_id('code_input').send_keys(verify1) # 输入图片验证码

driver.find_element_by_class_name('btn').click()  # 提交注册


#########################################K码分割线#############################
print('请输入K码！')
K_key = input()

driver.find_element_by_id('checkbox').click() # 接受协议

driver.find_element_by_class_name('input_x').send_keys(K_key) # 输入K码

driver.find_element_by_class_name('input_phone').send_keys(phone) # 输入手机号码

driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[3]/button').click() # 确认

######################################兑换分割线##################################
time.sleep(2)

driver.find_element_by_class_name('item-p').click()

driver.find_element_by_xpath('//*[@id="exchange"]/div[2]/button').click()

######################################验证码界面##################################

try:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'phonecodesend')))  # 判断是否加载
    driver.find_element_by_class_name('phonecodesend').click()
except:
    pass

print('请输入手机验证码')
verify_phone1 = input() # 第二次手机验证码

driver.find_element_by_class_name('phonecodeinput').send_keys(verify_phone1) # 输入手机验证码

driver.find_element_by_xpath('//*[@id="exchange"]/div[3]/div[1]/div[2]/div[4]').click() # 提交兑换








