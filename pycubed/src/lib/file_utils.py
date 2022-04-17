"""
`file_utils`
====================================================

CircuitPython utils for working with files asyncronously

* Author(s): 
 - Flynn Dreilinger

Implementation Notes
--------------------

"""
import os
from tasko.loop import _yield_once
import tasko
import time

def exists(file_name):
    try:
        os.stat(file_name)
    except Exception as e:
        if "[Errno 2] No such file/directory" in str(e):
            return False
        else:
            print(e)
    return True

class FileLockGuard(object):
    def __init__(self, file_name, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.file_name = file_name
        self.lock_name = file_name + ".lock"
    
    async def __aenter__(self):
        file = await self.lock_file()
        return file

    async def __aexit__(self, *args):
        self.unlock_file()

    async def lock_file(self):
        while True:
            # nobody has the lock, go for it
            if not exists(self.lock_name):
                # create lock file
                lock = open(self.lock_name, 'wb+')
                os.sync()
                lock.close()
                self.file = open(self.file_name, *self.args, **self.kwargs)
                return self.file # TODO fix this
            # someone else has the lock, yield to scheduler
            else:
                yield

    def unlock_file(self):
        if exists(self.lock_name):
            os.remove(self.lock_name)
            os.sync()
            self.file.close()
