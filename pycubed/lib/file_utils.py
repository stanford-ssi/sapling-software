import os
from tasko.loop import _yield_once
import tasko
import time

def exists(filename):
    try:
        os.stat(filename)
    except Exception as e:
        if "[Errno 2] No such file/directory" in str(e):
            return False
        else:
            print(e)
    return True

async def lock_file(filename):
    lock_name = filename + ".lock"
    while True:
        # nobody has the lock, go for it
        if not exists(lock_name):
            # create lock file
            f = open(lock_name, 'wb+')
            os.sync()
            f.close()
            return
        # someone else has the lock, yield to scheduler
        else:
            yield

def unlock_file(filename):
    lock_name = filename + ".lock"
    if exists(lock_name):
        os.remove(lock_name)
        os.sync()