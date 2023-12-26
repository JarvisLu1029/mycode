from multiprocessing import Process
import time

def print_numbers(start, end):
    for number in range(start, end + 1):
        print(number, end=', ', flush=True)
        time.sleep(1)


if __name__ == '__main__':
    process1 = Process(target=print_numbers, args=(1, 5))
    process2 = Process(target=print_numbers, args=(6, 10))

    process1.start() 
    process2.start()

    process1.join() 
    process2.join()

    print('執行結束')