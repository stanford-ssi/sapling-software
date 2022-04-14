from Tasks.template_task import Task
import time
import file_utils

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
            
            await file_utils.lock_file(filename)
            self.debug("task a: locked file")
            
            with open(filename, "w+") as f:
                for i in range(10):
                    f.write(f"hello world {i}\n")
                    self.debug("handing control to scheduler")
                    await self.cubesat.tasko.sleep(0.00001)

            file_utils.unlock_file(filename)
            assert(not file_utils.exists(filename + ".lock"))
            self.debug("ASSERT PASSED: task a has released lock")
            NEED_TO_WRITE_FILE = False
            yield

        else:
            pass