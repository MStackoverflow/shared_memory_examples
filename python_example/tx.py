# Python modules
from threading import Thread
from time import sleep
import os

# 3rd party modules
import posix_ipc
import mmap
import numpy as np

############################################################################
### Start a thread to count the number of time we change the values
### Note : time.sleep() is innacurate
counter=0
def count():
    global start,counter
    while 1:
        sleep(1)
        print(counter)
        counter=0

t = Thread(target=count, daemon=True)
t.start()
############################################################################

# Create the shared memory and the semaphore.
memory = None
try:
    memory = posix_ipc.SharedMemory("test_shared_memory", posix_ipc.O_CREX,
                                    size=2048)
except:
    memory = posix_ipc.SharedMemory("test_shared_memory")
try:
    semaphore = posix_ipc.Semaphore("test_semaphore", posix_ipc.O_CREX)
except:
    semaphore = posix_ipc.Semaphore("test_semaphore")

# Create an array
a = np.array([1, 2, 3, 4, 5, 6])

# Create a buffer that is linked to the shared memory
BUF = mmap.mmap(memory.fd, memory.size)

# Create an array that is memory mapped to the buffer that is the same size of the previous array
b = np.ndarray(a.shape, dtype=a.dtype, buffer=BUF)

# Put the array data into the buffer
b[:] = a[:] 

# we can close the share memory file and still use the mmap
os.close(memory.fd)

# release the semaphore if it was previously acquired
semaphore.release()

# Loop to change values in the array with semaphore lock
try:
    while 1:
        semaphore.acquire()
        b[0]=b[0]+1
        semaphore.release()
        counter=counter+1
    
# Clean when CTRL+C is done
except:
    semaphore.release()
    sleep(2)
    semaphore.acquire()
    posix_ipc.unlink_shared_memory("test_shared_memory")
    semaphore.release()
    semaphore.unlink()
    BUF.close()