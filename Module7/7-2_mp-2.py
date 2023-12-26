from multiprocessing import Process, Queue
import time


def split_num_into_sub_tasks(num):
    '''
    split into 4 sub tasks

    e.g. task 1 to 101 =>
    1, 26
    26, 51
    51, 76
    76, 101
    ''' 

    sub_tasks = []

    step = int(num / 4)
    for i in range(1, num, step):
        sub_tasks.append((i, i + step))
    
    return sub_tasks

def worker_process(start, end, result_queue):
    sum = 0
    for i in range(start, end):
        sum += i

    result_queue.put(sum)

def run_mp(num):
    result_queue = Queue()

    sub_tasks = split_num_into_sub_tasks(num)
    
    workers = []
    for sub_task in sub_tasks:
        worker = Process(target=worker_process,
                            args=(sub_task[0], sub_task[1], result_queue))
        workers.append(worker)
        worker.start()

    for w in workers:
        w.join() # 等待 Process 執行完畢

    sum = 0
    while not result_queue.empty():
        sum += result_queue.get()

    return sum


if __name__ == '__main__':
    start = time.time()

    sum = run_mp(100000001)

    print(sum)
    print("spend:", time.time() - start)