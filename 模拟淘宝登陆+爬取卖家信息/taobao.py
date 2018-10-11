import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from lxml import etree



print('请输入账号：')
username = input()
print('请输入密码：')
passworld = input()

driver = webdriver.Chrome()
driver.maximize_window()
driver.get('https://login.taobao.com/member/login.jhtml?redirectURL=http%3A%2F%2Ftrade.taobao.com%2Ftrade%2Fitemlist%2Flist_sold_items.htm%3Fspm%3Da313o.201708ban.category.d28.64f0197aAFB4S5%26mytmenu%3Dymbb')


js = """
    document.getElementById('TPL_username_1').value='{0}';
    document.getElementById('TPL_password_1').value='{1}';
    document.getElementById('J_SubmitStatic').click()
""".format(username, passworld)
driver.execute_script(js)

try:
    element = driver.find_element_by_id('nc_1__scale_text')
    ActionChains(driver).drag_and_drop_by_offset(element, 400, 0).perform()
    time.sleep(2)
    driver.execute_script(js)
except:
    print('无滑块')
    pass

time.sleep(3)
print('进入页面')
driver.switch_to.frame(0)

try:
    driver.find_element_by_id('J_GetCode').click()
    print('请输入手机验证码')
    x = input()
    driver.find_element_by_id('J_Phone_Checkcode').send_keys(x)
    driver.find_element_by_id('submitBtn').click()
except Exception as e:
    print(e)
    driver.execute_script("window.stop()")

time.sleep(3)
driver.refresh()

try:
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, 'page')))
except:
    print('over')
    driver.execute_script("window.stop()")

html = driver.page_source

selector = etree.HTML(html)

list1 = selector.xpath('//div[contains(@class,"item-mod__trade-order")]')

try:
    for i in list1:
        order_id = i.xpath('table[1]/tbody/tr/td[1]/label/span[3]/text()')[0] # 订单号
        order_time = i.xpath('table[1]/tbody/tr/td[1]/label/span[6]/text()')[0] # 下单时间
        price = i.xpath('table[2]/tbody/tr/td[2]/div/p/span[2]/text()')[0] # 价格
        all_price = i.xpath('table[2]/tbody/tr/td[7]/div/div[1]/p/strong/span[2]/text()')[0] # 总价
        saler_title = i.xpath('table[2]/tbody/tr/td[5]/div/p[1]/a/text()')[0] # 商品名
        name = i.xpath('table[2]/tbody/tr/td[5]/div/p[1]/a/text()')[0] # 买家账户名
        url = i.xpath('table[2]/tbody/tr/td[6]/div/div/p[1]/a/@href')[0] # 商品详情url
        url = 'https:' + url
        driver.get(url)
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="detail-panel"]/div/div[4]/div/ul/li[2]/a').click()
        address = driver.find_element_by_xpath('//*[@id="detail-panel"]/div/div[4]/div/div/div[2]/div/div/div[1]/div/span[2]/span').text # 发货地址（电话+ 地址 + 邮编）
        print(order_id, order_time, price, all_price, saler_title, name, address)
        ### 进入guimi进行举报操作
        driver.get('https://guimi.taobao.com')
        time.sleep(3)
        driver.find_element_by_xpath('/html/body/div[3]/div/div/a[2]').click()
        driver.find_element_by_xpath('//*[@id="J_Portal"]/div/div[1]/div[2]/a[1]').click()
        time.sleep(3)
        driver.find_element_by_id('order.0').send_keys(order_id)
        driver.find_element_by_xpath('//*[@id="root"]/div/div[3]/div[3]/div[2]/div/div/div[2]/div/div/button[4]').click()
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="root"]/div/div[3]/div[3]/div[2]/div/div/div[2]/div/div[2]/button').click()
        time.sleep(1)
        target = driver.find_element_by_xpath('//*[@id="root"]/div/div[3]/div[3]/div[3]/div[3]/div/div[3]/textarea')
        driver.execute_script("arguments[0].scrollIntoView();", target)
        target.send_keys('骗运费险的')
        driver.find_element_by_xpath('//*[@id="root"]/div/div[3]/div[3]/div[4]/button').click()

except Exception as e:
    print('程序异常错误:' + e)

finally:
    driver.quit()