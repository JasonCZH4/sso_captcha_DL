import numpy as np
import tensorflow as tf
from keras.applications.inception_v3 import InceptionV3
from tensorflow import keras
from tensorflow.keras import layers
from keras.optimizers import Adagrad, Adam, Nadam

def get_model():
    # inputs = keras.Input(shape=(50, 100, 1))
    base_model = InceptionV3(weights=None, include_top=False, input_shape=[75, 100, 1])  # 导入的inception_v3模型，去掉顶层和权重
    x = base_model.output
    x = layers.Reshape([32, 64, 1])(x)
    x = layers.Conv2D(16, 3, data_format='channels_last')(x)
    x = layers.Conv2D(16, 3, padding="same")(x)
    x = layers.PReLU()(x)
    x = layers.Conv2D(32, 3)(x)
    x = layers.Conv2D(32, 3, padding="same")(x)
    x = layers.PReLU()(x)
    x = layers.MaxPooling2D(3)(x)
    x = layers.Dropout(0.25)(x)

    x = layers.Conv2D(64, 3)(x)
    x = layers.Conv2D(64, 3, padding="same")(x)
    x = layers.ReLU()(x)
    x = layers.Conv2D(128, 3)(x)
    x = layers.Conv2D(128, 3, padding="same")(x)
    x = layers.ReLU()(x)
    x = layers.MaxPooling2D(3)(x)

    x = layers.Flatten()(x)
    x = layers.Dropout(0.5)(x)
    x = layers.Dense(4 * 36)(x)
    x = layers.Reshape([4, 36])(x)  # 4个符号，36个独热编码

    outputs = layers.Softmax()(x)
    model = keras.Model(inputs=base_model.inputs, outputs=outputs, name="captcha_model")
    model.compile(
        loss="categorical_crossentropy",
        optimizer=Adam(lr=0.0001),
        metrics=["accuracy"],
    )
    # print(model.summary())
    return model

# get_model()