# -*- encoding:utf-8 -*-
# @Time    : 2020/5/11 3:31 下午
# @Author  : jiang.g.f
# @File    : __init__.py
# @Software: PyCharm

from .str_process import rename_file_str, get_random_name

__all__ = ['rename_file_str', 'get_random_name']

# 相对路径其实指的是相对于最上层调用的模块，供他人调用的函数，慎用无前缀相对路径