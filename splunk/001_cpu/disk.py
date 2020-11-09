import random
import tempfile
import re
import os
import ctypes
import platform
import string


def formatSize(bytes):
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except:
        return "Error"

    if kb >= 1024:
        M = kb / 1024
        if M >= 1024:
            G = M / 1024
            return "%.2fG" % (G)
        else:
            return "%.2fM" % (M)
    else:
        return "%.2fkb" % (kb)


def getDiskFreeSpace(disk):
    """ Return disk free space (in bytes)
    """
    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(disk), None, None, ctypes.pointer(free_bytes))
        return formatSize(free_bytes.value)
    else:
        st = os.statvfs(disk)
        return formatSize(st.f_bavail * st.f_frsize)


def create_dummy(size_gb):
    file_size_in_gb = 0
    if '.' in size_gb:
        file_size_in_gb = re.findall(r"(\d+)\.", size_gb)[0]
    elif size_gb.endswith('G'):
        file_size_in_gb = size_gb.replace('G', '')
    filepath = os.path.join(tempfile.gettempdir(), str(random.randint(999,9999)))
    print("### Will create the file in the path: ", filepath)
    print("### Please delete the file manually: ", filepath)
    print("### Will fill the dummp file with size", file_size_in_gb, "GB")

    with open(filepath, "wb") as file:
        size_1gb = bytearray(1024 * 1024 * 1000)
        file.write(b"test")
        file.flush()
        for i in range(int(file_size_in_gb)):
            #file.seek(size_1gb*i)
            file.write(bytes(size_1gb))
            file.flush()


space = getDiskFreeSpace("/")
print("free space is ", space)

create_dummy(space)
