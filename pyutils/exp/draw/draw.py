# -*- encoding:utf-8 -*-
# @Time    : 2020/6/30 1:29 下午
# @Author  : jiang.g.f
# @File    : draw.py
# @Software: PyCharm
"""
绘制折线，可以有多种颜色及形状，c代表color，marker代表节点形状，ms代表marker size，label是折现名称。
plt.plot(x, y1, lw=1, c='red', marker='s', ms=4, label='Y1')
比如要控制y1为紫色线条，*状符号，就可以：
plt.plot(x, y1, lw=1, c='purple', marker='*', ms=4, label='Y1')

's' : 方块状
'o' : 实心圆
'^' : 正三角形
'v' : 反正三角形
'+' : 加好
'*' : 星号
'x' : x号
'p' : 五角星
'1' : 三脚架标记
'2' : 三脚架标记

"""
import numpy as np
import matplotlib.pyplot as plt

#从pyplot导入MultipleLocator类，这个类用于设置刻度间隔
from matplotlib.pyplot import MultipleLocator


x1 = ['v1', 'v2', 'v3', 'v4', 'v5']
end2end_image = [47.2, 48.6, 51.3, 53.1, 55.0]

x2 = ['v1', 'v2']
end2end_video = [31.1, 33.2]


x_major_locator = MultipleLocator(1)
ax = plt.gca()
ax.xaxis.set_major_locator(x_major_locator)


l1 = plt.plot(x1, end2end_image, c='r', marker='^', ms=12, label='end2end-image')
# l2 = plt.plot(x2, end2end_video, 'g--', label='end2end-video')

for a, b in zip(x1, end2end_image):
    plt.text(a, b+0.1, f'{b}%', ha='center', va= 'bottom', fontsize=12)

font_legend = {'family': 'Times New Roman', 'weight': 'normal', 'size': 14}
font_label = {'family': 'Times New Roman', 'weight': 'normal', 'size': 16}

plt.title('end2end-image model improvement')
plt.xlabel('version', font_label)
plt.ylabel('recall(3%)', font_label)
plt.tick_params()
plt.legend()

plt.show()
