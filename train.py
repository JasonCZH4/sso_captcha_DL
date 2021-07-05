import os
import time
from os.path import join
from data import cv_im_process, load_dataset, text2vec, vec2text
from model import get_model
import tensorflow as tf
from keras.callbacks import ModelCheckpoint

(x_train, t_train), (x_test, t_test) = load_dataset()

model = get_model()
checkpoint = ModelCheckpoint(filepath='./sso_image_1.h5', monitor='accuracy', mode='auto', save_best_only='True',
                             period=4)
history = model.fit(
    x_train,
    t_train,
    batch_size=128,
    epochs=2000,
    validation_split=0.2,
    callbacks=[checkpoint],
    shuffle=True)
test_scores = model.evaluate(x_test, t_test, verbose=2)
print("Test loss:", test_scores[0])
print("Test accuracy:", test_scores[1])
