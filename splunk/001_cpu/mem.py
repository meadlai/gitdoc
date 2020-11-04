import re
import multiprocessing
import time
import os

bool_has_mem = True
time_sleep_second = 1

cpu_count = multiprocessing.cpu_count()

def get_mem():
    if os.name == 'nt':
        print("Unable to get memory info in the windows")
        return

    with open('/proc/meminfo') as f:
        meminfo = f.read()
        print(meminfo)

    total_mem = re.search(r'MemTotal:\s+(\d+)', meminfo)
    free_mem = re.search(r'MemFree:\s+(\d+)', meminfo)

    if total_mem:
        mem_total_kB = int(total_mem.groups()[0])
        print("total memory is: ", mem_total_kB)
    if free_mem:
        mem_free_kB = int(free_mem.groups()[0])
        print("free memory is: ", mem_free_kB)

list_string = []

def task():
    global list_string
    try:
        eat_mem = bytearray(1024 * 1024 * 1000)
        list_string.append(eat_mem)
        print("try to allocate memory: 1GB, total is ", len(list_string), " GB")
        #wait_signal.wait()
    except MemoryError as ex:
        bool_has_mem = False
        print("Unable to allocate any memory in this system.")
        get_mem()


def process(num):
    print("Starting process: ", num)
    global bool_has_mem
    while bool_has_mem:
        print("running ", bool_has_mem)
        task()
        time.sleep(time_sleep_second)


if __name__ == "__main__":
    get_mem()
    process(0)
    '''
    for index in range(cpu_count):
        p = multiprocessing.Process(target=process, args=(index,))
        p.start()
    '''
