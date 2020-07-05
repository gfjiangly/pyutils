# -*- encoding:utf-8 -*-
# @Time    : 2020/7/3 4:45 下午
# @Author  : jiang.g.f
# @File    : multi_cls_to_binary.py
# @Software: PyCharm
import os
import tensorflow as tf
from tensorflow.keras.layers import Lambda
from tensorflow.python.keras import backend


os.environ["CUDA_VISIBLE_DEVICES"] = "0"

# set GPU memory
config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth=True
tf.compat.v1.Session(config=config)

version = tf.__version__
gpu_ok = tf.test.is_gpu_available()
print("tf version: {}, GPU {}".format(version, gpu_ok))


def binary_cls(x):
    neg = x[:, :1]
    pos = 1. - neg
    return tf.keras.layers.concatenate([neg, pos])


def binary_cls_output_shape(input_shape):
    shape = list(input_shape)
    assert len(shape) == 2  # only valid for 2D tensors
    shape[-1] = 2
    return tuple(shape)


def convert_multi_cls_model_to_binary_tf(model_path,
                                         output_path,
                                         output_model_format='tf'):
    base_model = tf.keras.models.load_model(model_path, custom_objects={"backend": backend})
    top_model = tf.keras.Sequential()
    top_model.add(Lambda(binary_cls, output_shape=binary_cls_output_shape))
    model = tf.keras.Model(inputs=base_model.input, outputs=top_model(base_model.output))
    model.save(output_path, save_format=output_model_format)
    return model

