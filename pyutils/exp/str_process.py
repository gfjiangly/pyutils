# -*- encoding:utf-8 -*-
# @Time    : 2020/5/11 3:31 下午
# @Author  : jiang.g.f
# @File    : str_process.py
# @Software: PyCharm
import sys
import os.path as osp
import random
import string
import time


def rename_file_str(file, prefix=None, suffix=None):
    dir_base = osp.split(file)
    name_ext = osp.splitext(dir_base[1])
    name = name_ext[0]
    if prefix is not None:
        name = prefix + name
    if suffix is not None:
        name = name + suffix
    return osp.join(dir_base[0], name+name_ext[1])


def get_random_name(random_len=28, time_len=4):
    # 随机输出8位由英文字符和数字组成的字符串 + 4位时间戳
    salt = ''.join(random.sample(string.ascii_letters + string.digits, random_len))
    salt += str(int(round(time.time() * 1000000)))[-time_len:]
    return salt


def get_cur_file_name():
    # 当前文件名，可以通过__file__获得
    # 绝对路径
    # print(__file__)
    # print(sys.argv[0])
    return sys._getframe().f_code.co_filename


def get_cur_f_name():
    # 当前函数名
    return sys._getframe().f_code.co_name


def get_cur_f_lineno():
    # 当前行号
    return sys._getframe().f_lineno