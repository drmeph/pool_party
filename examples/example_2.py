import time
import threading
import random

from queue import Queue
from poolParty import Worker


# Our logic to be performed Asynchronously
def my_process(a):
    t = threading.current_thread()
    time.sleep(random.uniform(0, 3))
    print(f'{t.getName()} has finished the task {a} ...')


def exception_handler(thread_name, exception):
    print(f'{thread_name, exception}')


# create a queue & pool.
q = Queue()
t = Worker(name='worker', queue=q, wait_queue=False, sleep=0.1, exception_handler=exception_handler)

# adding some tasks to the queue.
for i in range(10):
    my_task = (my_process, (i,), {})
    q.put(my_task)

try:
    # start the pool
    t.start()
    # block the code execution here to check the KeyboardInterrupt (to stop the worker safely)
    while t.is_alive():
        t.join(0.5)

    # can't go here until the worker finishes his work.

except (KeyboardInterrupt, SystemExit):
    # stop the Worker/thread.
    t.abort()
