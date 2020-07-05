# -*- encoding:utf-8 -*-
# @Time    : 2020/5/27 6:08 下午
# @Author  : jiang.g.f
# @File    : convert_multi_cls_model_to_binary.py
# @Software: PyCharm
import os
import argparse
import numpy as np
import mxnet as mx


def convert_fp16_to_fp32_mx(model_prefix, output_model_prefix, epoch):
    # convert fp16 to fp32
    symbol, arg_params, aux_params = mx.model.load_checkpoint(model_prefix, epoch)
    for key in arg_params:
        arg_params[key] = arg_params[key].astype(np.float32)
    for key in aux_params:
        aux_params[key] = aux_params[key].astype(np.float32)
    mx.model.save_checkpoint(output_model_prefix, epoch, symbol, arg_params, aux_params)


def convert_multi_cls_to_binary_mx(model_dir, model_name, num_workers, num_epochs):
    # output path
    fp32_model_dir = os.path.join(model_dir, 'fp32_binary_cls')
    if not os.path.exists(fp32_model_dir):
        os.makedirs(fp32_model_dir)
    
    for n in range(num_workers):
        
        if num_workers == 0:
            fp32_path = fp32_model_dir
        else:
            fp32_path = os.path.join(fp32_model_dir, str(n))
            if not os.path.exists(fp32_path):
                os.makedirs(fp32_path)
        
        # when worker id is zero, model name has no zero
        if n > 0:
            model_prefix = os.path.join(model_dir, model_name + '-' + str(n))
            fp32_model_prefix = os.path.join(fp32_path, model_name + '-' + str(n))
        else:
            model_prefix = os.path.join(model_dir, model_name)
            fp32_model_prefix = os.path.join(fp32_path, model_name)

        # Batch evaluation currently does not support float16, so ...
        for e in range(num_epochs):
            if os.path.isfile('{}-{:04d}.params'.format(model_prefix, e+1)):
                convert_fp16_to_fp32_mx(model_prefix, fp32_model_prefix, e+1)
        
        print('single task, convert {} to binary-cls symbol'.format(fp32_model_prefix))

        symbol = fp32_model_prefix + '-symbol.json'
        sym = mx.sym.load(symbol)
        
        internals = sym.get_internals()
        sym = internals['rgb_cast3_output']
        sym = mx.sym.softmax(sym)
        class0 = mx.sym.slice(sym, begin=(None, 0), end=(None, 1))
        class1 = 1 - class0
        rgb_cnn_softmax = mx.sym.concat(class0, class1, dim=1, name='rgb_cnn_softmax')
        rgb_cnn_softmax.save(symbol)
        
        # replace float32 to float16 in symbol.json
        # for compatibility with py2, using os.system to call shell cmd
        os.system('sed -i "s/float16/float32/g" {}'.format(symbol))
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_dir', required=True)
    parser.add_argument('--model_name', required=True)
    parser.add_argument('--num_epochs', type=int, required=True)
    parser.add_argument('--num_workers', type=int, default=0)
    args = parser.parse_args()
    
    convert_multi_cls_to_binary_mx(args.model_dir, args.model_name, args.num_workers, args.num_epochs)
