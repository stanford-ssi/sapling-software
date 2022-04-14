from Tasks.template_task import Task
import time
import file_utils

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
            await file_utils.lock_file("/sd/LOCKING_TEST_FILE")
            self.debug("task b: locked file")
            
            with open("/sd/LOCKING_TEST_FILE", 'r') as f:
                for line in f:
                    self.debug(line)
            
            file_utils.unlock_file("/sd/LOCKING_TEST_FILE")
            assert(not file_utils.exists(filename + ".lock"))
            self.debug("ASSERT PASSED: task b has released lock")
            self.debug('test stop: {}'.format(time.monotonic()))
            NEED_TO_PRINT_FILE = False
            self.debug("TEST PASSED")

        else:
            pass
