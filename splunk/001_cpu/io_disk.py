import multiprocessing
import threading
import math
import time
import datetime


cpu_count = multiprocessing.cpu_count()
print(" the CPU count in this machine is ", cpu_count)


def task():
    percent_cpu = 80
    cpu_time_rest = float(100 - percent_cpu)
    while True:
        start_time = datetime.datetime.now()
        while (datetime.datetime.now() - start_time).microseconds > cpu_time_rest*1000:
            math.factorial(100)
        #time.sleep(cpu_time_rest/1000)


def process(num):
    print("Starting process: ", num)
    for index in range(cpu_count):
        thread = threading.Thread(target=task())
        thread.daemon = True
        thread.start()


if __name__ == "__main__":
    for index in range(cpu_count):
        p = multiprocessing.Process(target=process, args=(index,))
        p.start()







