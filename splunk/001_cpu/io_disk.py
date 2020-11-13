import multiprocessing
from random import shuffle
import os
import sys
import random
import time


cpu_count = multiprocessing.cpu_count()
print(" the CPU count in this machine is ", cpu_count)

# this program will do writing-reading in multiply-process/threading
# loop count: loop 5 times in each thread
loop_count = 5
multiply_cpu_core = 3
# file count: write or
file_count = 18

if cpu_count < 6:
    # set 15 files
    pass
else:
    file_count = cpu_count * multiply_cpu_core


class LowLevel:

    def __init__(self, file, write_mb, write_block_kb, read_block_b):
        self.write_mb = write_mb
        self.write_block_kb = write_block_kb
        self.read_block_b = read_block_b
        wr_blocks = int(self.write_mb * 1024 / self.write_block_kb)

        abs_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file = os.path.join(abs_path, file)
        self.file = file
        print("### Will create the file in the path: ", file)
        #
        if not os.path.exists(file):
            with open(file, 'w'):
                pass
        rd_blocks = int(self.write_mb * 1024 * 1024 / self.read_block_b)
        for i in range(loop_count):
            self._write_test(1024 * self.write_block_kb, wr_blocks)
            self._read_test(self.read_block_b, rd_blocks)
            os.remove(self.file)
            time.sleep(random.random())

    def _write_test(self, block_size, blocks_count, show_progress=False):
        '''
        Performs write with low level API
        '''
        f = os.open(self.file, os.O_CREAT | os.O_WRONLY, 0o777)  # low-level I/O

        took = []
        for i in range(blocks_count):
            if show_progress:
                # dirty trick to actually print progress on each iteration
                sys.stdout.write('\rWriting: {:.2f} %'.format(
                    (i + 1) * 100 / blocks_count))
                sys.stdout.flush()
            buff = os.urandom(block_size)
            os.write(f, buff)
            os.fsync(f)  # force write to disk
        # close it in the end
        os.close(f)

    def _read_test(self, block_size, blocks_count, show_progress=False):
        '''
        Performs read with low level API
        '''
        f = os.open(self.file, os.O_RDONLY, 0o777)  # low-level I/O
        # generate random read positions
        offsets = list(range(0, blocks_count * block_size, block_size))
        shuffle(offsets)

        for i, offset in enumerate(offsets, 1):
            if show_progress and i % int(self.write_block_kb * 1024 / self.read_block_b) == 0:
                sys.stdout.write('\rReading: {:.2f} %'.format(
                    (i + 1) * 100 / blocks_count))
                sys.stdout.flush()
            os.lseek(f, offset, os.SEEK_SET)  # set position
            buff = os.read(f, block_size)  # read from position
            if not buff: break  # if EOF reached
        os.close(f)

    def print_result(self):
        result = ('\n\nWritten {} MB \n'.format(self.write_mb))
        result += ('\nRead {} B blocks\n'.format(self.read_block_b))
        print(result)


class HighLevel:

    def __init__(self, file):
        abs_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file = os.path.join(abs_path, file)
        self.file = file
        print("### Will create the file in the path: ", file)
        #
        if not os.path.exists(file):
            with open(file, 'w'):
                pass

        for i in range(loop_count):
            self._write_test()
            self._read_test()
            os.remove(self.file)
            time.sleep(random.random())

    def _write_test(self):
        with open(self.file, "wb") as file:
            size_1gb = bytearray(1024 * 1024 * 1024)
            file.write(bytes(size_1gb))
            file.flush()
            file.close()

    def _read_test(self):
        piece_size = 1024*1024*300  # 1 KiB * 100 ~= 100M
        with open(self.file, "rb") as file:
            piece = file.read(piece_size)
            while piece:
                piece = file.read(piece_size)
                if piece == "":
                    break  # end of file
                if piece is None:
                    break  # end of file
                if piece == "b''":
                    break  # end of file
        file.close()

    def print_result(self):
        print("Written and Read in High-Level API")


def process(num):
    print("Starting process: ", num)
    normal_io_file_size_in_gb = 1
    if num%2 == 0:
        low_level = LowLevel("disk_low_level_test_file_" + str(num) + ".data", 1024, 1024, 512)
        low_level.print_result()
        pass
    else:
        high_level = HighLevel("disk_high_level_test_file_" + str(num) + ".data")
        high_level.print_result()


if __name__ == "__main__":

    for index in range(file_count):
        p = multiprocessing.Process(target=process, args=(index,))
        p.start()






