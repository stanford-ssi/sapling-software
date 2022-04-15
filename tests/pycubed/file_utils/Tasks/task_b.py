from Tasks.template_task import Task
import time
from file_utils import FileLockGuard, exists

NEED_TO_PRINT_FILE = True

class task(Task):
    priority = 2
    frequency = 10 # once every 1s
    name = 'test b'
    color = 'red'

    schedule_later = True

    async def main_task(self):
        global NEED_TO_PRINT_FILE
        
        if NEED_TO_PRINT_FILE:
            self.debug("trying to lock file")

            filename = "/sd/LOCKING_TEST_FILE"
            
            async with FileLockGuard(filename, 'r') as f:
                self.debug("locked file")
                for line in f:
                    self.debug(line.strip())

            self.debug("unlocked file")
            assert(not exists(filename + ".lock"))
            self.debug("ASSERT PASSED: task b has released lock")
            self.debug('test stop: {}'.format(time.monotonic()))
            NEED_TO_PRINT_FILE = False
            self.debug("TEST PASSED")

        else:
            pass
