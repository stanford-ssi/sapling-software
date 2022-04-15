from Tasks.template_task import Task
import time
from file_utils import FileLockGuard, exists

NEED_TO_WRITE_FILE = True

class task(Task):
    priority = 1
    frequency = 10 # once every 1s
    name = 'test a'
    color = 'blue'

    schedule_later = True

    async def main_task(self):
        global NEED_TO_WRITE_FILE
        
        if NEED_TO_WRITE_FILE:
            self.debug('test start: {}'.format(time.monotonic()))
            
            filename = "/sd/LOCKING_TEST_FILE"
            
            async with FileLockGuard(filename, "w+") as f:
                self.debug("locked file")
                for i in range(10):
                    f.write(f"hello world {i}\n")
                    self.debug("wrote to file, passed control to handler")
                    yield
            self.debug("unlocked file")
            assert(not exists(filename + ".lock"))
            self.debug("ASSERT PASSED: task a has released lock")
            NEED_TO_WRITE_FILE = False
            yield

        else:
            pass