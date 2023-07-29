# Python modules
import mmap
import os
import sys
import hashlib
from time import sleep
from threading import Thread
from time import sleep
# 3rd party modules
import posix_ipc
import numpy as np
from multiprocessing import shared_memory
# Utils for this demo
import utils

existing_shm = shared_memory.SharedMemory(name="test")
c = np.ndarray((6,), dtype=np.int32, buffer=existing_shm.buf)
utils.say("Oooo 'ello, I'm Mrs. Conclusion!")

params = utils.read_params()

# Mrs. Premise has already created the semaphore and shared memory.
# I just need to get handles to them.
memory = posix_ipc.SharedMemory(params["SHARED_MEMORY_NAME"])
semaphore = posix_ipc.Semaphore(params["SEMAPHORE_NAME"])

# MMap the shared memory
mapfile = mmap.mmap(memory.fd, memory.size)

# Once I've mmapped the file descriptor, I can close it without
# interfering with the mmap. This also demonstrates that os.close() is a
# perfectly legitimate alternative to the SharedMemory's close_fd() method.
os.close(memory.fd)

what_i_wrote = ""

counter=0
def count():
    global start,counter
    while 1:
        sleep(1)
        print(counter)
        counter=0

t = Thread(target=count, daemon=True)
#t.start()

try:
    while 1:
        print(c)
        sleep(1)

except:
    semaphore.release()
    semaphore.close()
    mapfile.close()

    utils.say("")
    print("fin")
