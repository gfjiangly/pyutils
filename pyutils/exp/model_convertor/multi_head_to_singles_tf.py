# -*- encoding:utf-8 -*-
# @Time    : 2020/7/3 4:44 下午
# @Author  : jiang.g.f
# @File    : multi_head_to_singles.py
# @Software: PyCharm
import os.path as osp
import tensorflow as tf
from tensorflow.python.keras import backend


def convert_multi_head_to_multi_models(model_path,
                                       save_path,
                                       save_name,
                                       save_format='h5'):
    outputs = []
    if save_format == 'h5':
        # base_model = load_keras_model_from_h5(model_path)
        base_model = tf.keras.models.load_model(
            model_path, custom_objects={"backend": backend})
        num_head = len(base_model.outputs)
        for i, output in enumerate(base_model.outputs):
            sub_model = tf.keras.Model(base_model.inputs, outputs=output)
            # out_name = 'head{}_{}cls'.format(i, output.shape[1])
            out_name = 'head_{}cls_model'.format(output.shape[1])
            cls_path = osp.join(save_path, out_name, save_name)
            sub_model.save(cls_path, save_format='tf')
            if out_name not in outputs:
                outputs.append(out_name)
    elif save_format == 'saved_model':
        base_model = tf.keras.models.load_model(
            model_path, custom_objects={"backend": backend})
        for i, output in enumerate(base_model.outputs):
            sub_model = tf.keras.Model(base_model.inputs, outputs=output)
            # out_name = 'head{}_{}cls'.format(i, output.shape[1])
            out_name = 'head_{}cls_model'.format(output.shape[1])
            cls_path = osp.join(save_path, out_name, save_name)
            sub_model.save(cls_path, save_format='tf')
            if out_name not in outputs:
                outputs.append(out_name)
    else:
        raise NotImplementedError(
            "This format model({}) does not support conversion!".format(save_format))
    return outputs