# Python modules
from threading import Thread
from time import sleep
import os
# 3rd party modules
import posix_ipc
import mmap
import numpy as np

# Create the shared memory and the semaphore.
memory = None
try:
    memory = posix_ipc.SharedMemory("TESTSMH", posix_ipc.O_CREX,
                                    size=1024)
except:
    memory = posix_ipc.SharedMemory("TESTSMH")
try:
    semaphore = posix_ipc.Semaphore("TESTSEMA", posix_ipc.O_CREX)
except:
    semaphore = posix_ipc.Semaphore("TESTSEMA")

a = np.array([1, 1, 2, 3, 5, 8])
BUF = mmap.mmap(memory.fd, memory.size)
b = np.ndarray(a.shape, dtype=a.dtype, buffer=BUF)
b[:] = a[:] 

os.close(memory.fd)

print(b)
counter=0
def count():
    global start,counter
    while 1:
        sleep(1)
        print(counter)
        counter=0

t = Thread(target=count, daemon=True)
t.start()
semaphore.release()
try:
    while 1:
        semaphore.acquire()
        b[0]=b[0]+1
        semaphore.release()
        counter=counter+1
    
    
except:
   
    semaphore.release()
    sleep(2)
    semaphore.acquire()
    posix_ipc.unlink_shared_memory("TESTSMH")
    semaphore.release()
    semaphore.unlink()
    BUF.close()