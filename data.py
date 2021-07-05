import numpy as np
import cv2
import os
from os import listdir
from os.path import isfile, join
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.callbacks import EarlyStopping, Callback as TfCallback

marked_path = r'C:\Users\ASUS\PycharmProjects\AI_Image\sso_image\scnu-sso-captcha-master\src\dataset\codes\small_mark/'
files = [f for f in listdir(marked_path)]
np.random.shuffle(files)


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


idict = '0123456789abcdefghijklmnopqrstuvwxyz'


def text2vec(code):  # ont-hot编码
    code = code.lower()
    print(code)
    t = np.zeros((len(code), 36), np.float)
    for i in range(t.shape[0]):
        t[i][idict.index(code[i])] = 1
    return t


def vec2text(t):
    idx = np.argmax(t, axis=1)
    b = ""
    for i in idx:
        b += idict[i]
    return b


def load_dataset():
    x_all = []
    t_all = []
    for code in files:
        file_path = join(marked_path, code)  # 组成完整路径
        code = code.split('.')[0]  # 取.前面的字符串
        img = cv_im_process(cv2.imread(file_path), flatten=False, normalize=True)  # 读取并处理
        t = text2vec(code)  # 变成独热编码
        x_all.append(img)  # 图片
        t_all.append(t)  # 标签
    x_all = np.array(x_all)
    t_all = np.array(t_all)
    # print(x_all.shape, t_all.shape)
    # print('x element shape', x_all[0].shape)
    # print('label element shape',t_all[0].shape)

    total_size = x_all.shape[0]
    test_size = min(int(total_size / 10), 500)
    train_size = int(total_size - test_size)
    # print(total_size, test_size)
    x_train = x_all[:train_size]  # 训练集
    t_train = t_all[:train_size]
    x_test = x_all[train_size:]  # 测试集
    t_test = t_all[train_size:]
    # print('training set', x_train.shape, t_train.shape)
    return (x_train, t_train), (x_test, t_test)


load_dataset()
