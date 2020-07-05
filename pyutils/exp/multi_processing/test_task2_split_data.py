# -*- encoding:utf-8 -*-
# @Time    : 2020/5/28 10:09 上午
# @Author  : jiang.g.f
# @File    : test_task2_split_data.py
# @Software: PyCharm
import os
import os.path as osp
import pyutils
import multiprocessing as mp
import queue as queue

from .produce_consume import MultiTask

logger = pyutils.get_logger()


def load(q, data, woker_id=0, display=10000):
    """单进程处理，无时间瓶颈"""
    count = 0
    if not isinstance(data, list):
        data = [data]
    for file in data:
        with open(file, 'r') as reader:
            line = reader.readline()
            if 'vid' in line:
                line = reader.readline()
            while line:
                # time.sleep(0.0001)
                q.put(line)
                line = reader.readline()
                count += 1
                if count % display == 0:
                    logger.info('load {} items by worker{}'.format(count, woker_id))
    q.put(None)


def consume(q, woker_id=0, finished=None, head=None, save_path='./', display=1000):
    """多进程，有时间瓶颈"""
    count = 0
    save_file = osp.join(save_path, 'split{}.tsv'.format(woker_id))
    with open(save_file, 'w') as writer:
        writer.write(head)
        while finished.value == 0:
            try:
                result = q.get(timeout=5)
                if result is None:
                    finished.value = 1
                    break
                writer.write(result)
                count += 1
                if count % display == 0:
                    print('saved {} items by worker{}'.format(count, woker_id))
            except queue.Empty:
                print('waiting for reading items...')
    print('saved {} items in {}!'.format(count, save_file))


if __name__ == '__main__':
    from functools import partial
    data = [
        'xxx.yyy'
    ]
    save_path = 'yyy.xxx'
    if not os.path.isdir(save_path):
        os.makedirs(save_path)
    # 使用partial修改函数默认值，传入运行时参数
    finished = mp.Value("I", 0)
    consume = partial(consume, finished=finished, head='vid\tlabel\n', save_path=save_path)
    task = MultiTask(load, consume=consume, consumer_workers=2500)
    task.run(data)