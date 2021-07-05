# Author:JasonCZH4
# Date:2021/3/28 17:29
import re
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import tesserocr
# from predict import predict_ans as pa
from selenium import webdriver
import json
from selenium import webdriver
from selenium.webdriver import ActionChains
import json
import time
import time
import pyautogui

from keras.models import load_model
import cv2
import numpy as np

def cv_im_process(img, flatten=False, normalize=False):
    img = cv2.resize(img, (100, 75), interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 转换为灰度图
    # 二值化
    im2 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 15)
    # 去除噪点，尤其是椒盐噪点
    im3 = cv2.medianBlur(im2, 3)
    # 线降噪
    h, w = im3.shape[:2]
    for y in range(1, w - 1):
        for x in range(1, h - 1):
            count = 0
            if np.all(im3[x, y - 1] > 245):
                count = count + 1
            if np.all(im3[x, y + 1] > 245):
                count = count + 1
            if np.all(im3[x - 1, y] > 245):
                count = count + 1
            if np.all(im3[x + 1, y] > 245):
                count = count + 1
            if count > 2:
                im3[x, y] = 255
    im3 = im3
    if flatten:
        im3 = im3.flatten()
    if normalize:
        im3 = im3 / 255
    return im3


model = load_model(r'C:\Users\ASUS\PycharmProjects\AI_Image\sso_image\sso_image.h5')

idict = '0123456789abcdefghijklmnopqrstuvwxyz'
def vec2text(t):
    idx = np.argmax(t, axis=1)
    b = ""
    for i in idx:
        b += idict[i]
    return b
def predict_ans():
    # print(model.summary())
    file_path = r'C:\Users\ASUS\PycharmProjects\AI_Image\sso_image\scnu_11.jpg'
    x = cv_im_process(cv2.imread(file_path), flatten=False, normalize=True)
    p = model.predict(np.array([x]))
    return  vec2text(p[0])


cnt = 0
for i in range(50):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 '
                      'Safari/537.36 QIHU 360SE', 'Connection': 'keep-alive',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}
    # result = requests.get('https://sso.scnu.edu.cn/AccountService/user/rancode.jpg?m=1.0024973463803444', headers=headers)
    # result = requests.get('https://sso.scnu.edu.cn/AccountService/user/index.html', headers=headers)


    options = webdriver.ChromeOptions()  # 创建一个配置对象
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE')  # 替换User-Agent

    # 1. 获取浏览器对象
    browser = webdriver.Chrome(options=options)
    # 2. 请求url
    url = "https://sso.scnu.edu.cn/AccountService/user/login.html"
    # 3. 窗口最大化
    browser.maximize_window()
    browser.get(url)
    # 4.点击搜索框
    time.sleep(1)
    box1 = browser.find_element_by_id("account")
    box1.click()
    box1.send_keys("20202133026")


    box2 = browser.find_element_by_id("password")
    box2.click()
    box2.send_keys("CZH@hs141804")



    im = pyautogui.screenshot(region=(1730, 655, 120, 60))
    im.save(r'C:/Users\ASUS\PycharmProjects\AI_Image\sso_image\scnu_11.jpg')

    ans = predict_ans()
    print(ans)

    box3 = browser.find_element_by_id("rancode")
    box3.click()
    box3.send_keys(ans)

    pyautogui.click(1600, 755)
    time.sleep(3)
    # print(pyautogui.pixel(1246, 186)

    if not pyautogui.pixelMatchesColor(1246, 186, (220, 66, 79), tolerance=50):
        pass
        '''
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
        '''
    else:
        cnt += 1
        print(cnt/(i+1))
        browser.close()
        # break
print(cnt)
print(cnt/50)
