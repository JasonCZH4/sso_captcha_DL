from keras.models import load_model
import cv2
import numpy as np
from data import cv_im_process, load_dataset, text2vec, vec2text

def cv_im_process(img, flatten=False, normalize=False):
    img = cv2.resize(img, (100, 75), interpolation=cv2.INTER_AREA)  # 修改尺寸
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

def vec2text(t):
    idx = np.argmax(t, axis=1)
    b = ""
    for i in idx:
        b += idict[i]
    return b


def predict_ans():
    model = load_model(r'C:\Users\ASUS\PycharmProjects\AI_Image\sso_image\sso_image.h5')  # 加载模型
    # print(model.summary())
    (x_train, t_train), (x_test, t_test) = load_dataset()
    test_scores = model.evaluate(x_test, t_test, verbose=2)
    print("Test loss:", test_scores[0])
    print("Test accuracy:", test_scores[1])
    file_path = r'C:\Users\ASUS\PycharmProjects\AI_Image\sso_image\scnu_11.jpg'
    x = cv_im_process(cv2.imread(file_path), flatten=False, normalize=True)
    p = model.predict(np.array([x]))
    return vec2text(p[0])

predict_ans()