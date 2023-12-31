# Python modules
import mmap
import os
from threading import Thread
from time import sleep
# 3rd party modules
import posix_ipc
import numpy as np


# Mrs. Premise has already created the semaphore and shared memory.
# I just need to get handles to them.
memory = posix_ipc.SharedMemory("test_shared_memory")
semaphore = posix_ipc.Semaphore("test_semaphore")

BUF = mmap.mmap(memory.fd, memory.size)
c = np.ndarray((6,), dtype=np.int32, buffer=BUF)

os.close(memory.fd)

counter=0
def count():
    global start,counter
    while 1:
        sleep(1)
        print(counter)
        counter=0

t = Thread(target=count, daemon=True)
t.start()

try:
    while 1:
        semaphore.acquire()
        c[1]=c[1]+1
        #sleep(1) # Remove comments to verify that the semaphore is working properly
        semaphore.release()
        counter=counter+1
        #sleep(0)

except:
    semaphore.release()
    semaphore.close()
    BUF.close()
    print("fin")