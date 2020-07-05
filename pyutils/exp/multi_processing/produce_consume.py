# -*- encoding:utf-8 -*-
# @Time    : 2020/5/14 8:45 下午
# @Author  : jiang.g.f
# @File    : produce_consume.py.py
# @Software: PyCharm
import math
import multiprocessing as mp

MAX_QUEUE_SIZE = 1024


def default_process(input_queue, output_queue, worker_id=0):
    """only get data from input_queue and put data to output_queue"""
    item = input_queue.get()
    while item is not None:
        output_queue.put(item)
        item = input_queue.get()
    output_queue.put(None)


"""有几种模式：
    1. 单生产者，单消费者
    2. 单生产者，多消费者
    3. 多生产者，单消费者
    4. 多生产者，多消费者

    生产者可分为两种形态：
    1. 数据加载即生产
    2. 数据加载和处理

    数据加载(或处理)的两种形态：
    1. 根据文件数分配进程
    2. 根据指定线程数，分配需要数量的数据量
"""


class MultiTask:
    
    def __init__(self, load, consume, product=None,
                 load_workers=1, product_workers=1, consumer_workers=1,
                 max_queue_size=MAX_QUEUE_SIZE):
        self.load = load
        self.consume = consume
        self.product = product
        self.load_workers = load_workers
        self.process_workers = product_workers
        self.consumer_workers = consumer_workers
        self.max_queue_size = max_queue_size
        self.processes = []
        self.input_queue = mp.Queue(self.max_queue_size)
        self.result_queue = mp.Queue(self.max_queue_size)
    
    def loader(self, data, **args):
        size = math.ceil(len(data) / self.load_workers)
        for idx in range(self.load_workers):
            process = mp.Process(
                target=self.load,
                args=(self.input_queue, data[idx * size:(idx + 1) * size], idx, *args))
            process.daemon = True
            process.start()
            self.processes.append(process)
    
    def producer(self, **args):
        for idx in range(self.process_workers):
            process = mp.Process(
                target=self.product,
                args=(self.input_queue, self.result_queue, idx, *args))
            process.daemon = True
            process.start()
            self.processes.append(process)
    
    def consumer(self, **args):
        for idx in range(self.consumer_workers):
            consume_process = mp.Process(
                target=self.consume,
                args=(self.result_queue if self.product is not None else self.input_queue, idx, *args))
            consume_process.daemon = True
            consume_process.start()
            self.processes.append(consume_process)
    
    def run(self, data, **args):
        if len(data) < self.load_workers:
            print('len(data) < load_workers, set load_workers={}'.format(len(data)))
            self.load_workers = len(data)
        self.loader(data, *args)
        if self.product is not None:
            self.producer(*args)
        self.consumer(*args)
        for p in self.processes:
            p.join()
