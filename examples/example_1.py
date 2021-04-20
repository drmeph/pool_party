import threading
import time
import random

from queue import Queue
from poolParty import Pool


def my_process(a):
    t = threading.current_thread()
    time.sleep(random.uniform(0, 3))
    print(f'{t.getName()} has finished the task {a} ...')


def exception_handler(thread_name, exception):
    print(f'{thread_name}: {exception}')


# create a queue & pool
q = Queue()
p = Pool(name='Pool_1', queue=q, max_workers=2, wait_queue=False, exception_handler=exception_handler)

# adding some tasks to the queue
for i in range(10):
    # task is a tuple of a function, args and kwargs
    my_task = (my_process, (i,), {})
    q.put(my_task)

try:
    # start the pool
    p.start()
    # go back to the main thread from time to another to check the KeyboardInterrupt
    while p.is_alive():
        p.join(0.5)

except(KeyboardInterrupt, SystemExit):
    # shutdown the pool by aborting its Workers/threads.
    p.shutdown()
