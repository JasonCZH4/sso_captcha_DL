# Author:JasonCZH4
# Date:2021/7/3 20:29
from predict import predict_ans as pa
import time
import pyautogui
from selenium import webdriver


options = webdriver.ChromeOptions()  # 创建一个配置对象
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE')  # 替换UA头

# 1. 获取浏览器对象
browser = webdriver.Chrome(options=options)
# 2. 请求url
url = "https://sso.scnu.edu.cn/AccountService/user/login.html"
# 3. 窗口最大化
browser.maximize_window()
browser.get(url)
# 4.点击输入框
time.sleep(1)
box1 = browser.find_element_by_id("account")  # 账号
box1.click()
box1.send_keys("your_account")


box2 = browser.find_element_by_id("password")  # 密码
box2.click()
box2.send_keys("your_password")

im = pyautogui.screenshot(region=(1730, 655, 120, 60))  # 验证码截图
im.save(r'C:/Users\ASUS\PycharmProjects\AI_Image\sso_image\scnu_11.jpg')  # 验证码保存

ans = pa()
print(ans)

box3 = browser.find_element_by_id("rancode")
box3.click()
box3.send_keys(ans)

pyautogui.click(1600, 755)
time.sleep(3)

for i in range(3):
    if not pyautogui.pixelMatchesColor(1246, 186, (220, 66, 79), tolerance=50):
        pyautogui.click(1215, 632)
        im = pyautogui.screenshot(region=(1730, 655, 120, 60))
        im.save(r'C:/Users\ASUS\PycharmProjects\AI_Image\sso_image\scnu_11.jpg')
        ans = pa()
        print(ans)
        box3 = browser.find_element_by_id("rancode")
        box3.clear()
        box3.click()
        box3.send_keys(ans)
        pyautogui.click(1600, 755)
        time.sleep(3)

    else:
        break
