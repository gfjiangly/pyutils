# -*- encoding:utf-8 -*-
# @Time    : 2020/6/12 5:35 下午
# @Author  : jiang.g.f
# @File    : test_task3_merge_kvdataset.py
# @Software: PyCharm
import argparse
from dataloader import KVReader, KVWriter

from .produce_consume import MultiTask


def load(q, data_path, worker_id=0, batch_size=64, num_reader=1, display=100):
    count = 0
    for path in data_path:
        reader = KVReader(path, num_reader)
        keys = reader.list_keys()
        for i in range(0, len(keys), batch_size):
            try:
                # print(i, keys[i:i+batch_size])
                values = reader.read_many(keys[i:i+batch_size])
                q.put((keys[i:i+batch_size], values))
            except Exception as e:
                print('='*10, 'read error! {}'.format(e))
                continue
            count += 1
            if count % display == 0:
                print('load {} items by worker{}'.format(count, worker_id))
        q.put(None)
    

def consume(q, worker_id=0, num_workers=1, to_path='./dataset',
            num_shard=1, display=100, flush_size=1000):
    num_working = num_workers
    writer = KVWriter(to_path + str(worker_id), num_shard)
    count = 0
    key_set = set()
    while num_working > 0:
        try:
            result = q.get(timeout=3)
            if result is None:
                num_working = num_working - 1
            else:
                filtered_keys = []
                filtered_values = []
                for key, value in zip(result[0], result[1]):
                    # print(key)
                    if key not in key_set:
                        filtered_keys.append(key)
                        filtered_values.append(value)
                        key_set.add(key)
                writer.write_many(filtered_keys, filtered_values)
                count += 1
                if count % flush_size == 0:
                    writer.flush()
                if count % display == 0:
                    print('saved {} example by worker{}'.format(count, worker_id))
        except Exception as e:
            print('waitting for reading examples...')
    writer.flush()  # Make sure to flush at the end
    print('saved {} examples in {}!'.format(count, to_path))


def parse_args():
    parser = argparse.ArgumentParser(
        "Merge KVDataset", conflict_handler='resolve', fromfile_prefix_chars='@')
    parser.add_argument(
        '--data_path',
        type=str,
        required=True,
        help='KVDataset path')
    parser.add_argument(
        '--out',
        type=str,
        required=True,
        help='File to store splited tar result')
    parser.add_argument(
        '--num_split',
        type=int,
        required=True,
        help='Number of KVDataset')
    
    # read
    parser.add_argument('--num_read_workers', type=int, default=32)
    parser.add_argument('--readers_per_worker', type=int, default=1)
    parser.add_argument('--read_batch_size', type=int, default=32)
    parser.add_argument('--read_display',type=int, default=100)  # batch
    parser.add_argument('--max_queue_size', type=int, default=1024)
    
    # write
    parser.add_argument('--num_split_of_saving', type=int, default=1)
    parser.add_argument('--write_num_shard',type=int, default=1)
    parser.add_argument('--write_display', type=int, default=100)
    parser.add_argument('--flush_size', type=int, default=1000)

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    dataset_to_merge = []
    for i in range(args.num_split):
        dataset_to_merge.append(args.data_path + str(i))

    from functools import partial
    load = partial(load,
                   num_reader=args.readers_per_worker,
                   batch_size=args.read_batch_size,
                   display=args.read_display)
    consume = partial(consume,
                      to_path=args.out,
                      num_shard=args.write_num_shard,
                      num_workers=args.num_read_workers,
                      display=args.write_display,
                      flush_size=args.flush_size)
    task = MultiTask(load, consume=consume,
                     load_workers=args.num_read_workers,
                     consumer_workers=args.num_split_of_saving,
                     max_queue_size=args.max_queue_size)
    task.run(dataset_to_merge)
