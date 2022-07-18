from Tasks.template_task import Task
from protocol_shared import aptp, ftp
from file_utils import FileLockGuard
import gc

class task(Task):
    priority = 1
    frequency = 10 # once every 1s
    name = 'test task'
    color = 'red'

    schedule_later = True

    async def main_task(self):
        inbox = aptp.inbox
        outbox = aptp.outbox
        f1 = FileLockGuard('/sd/tree.png')
        f1.unlock_file()
        del f1

        f2 = FileLockGuard('/sd/hello.txt')
        f2.unlock_file()
        del f2
        gc.collect()
        
        while True:
            packet = await inbox.get()
            #print(packet)
            if packet:
                break
            yield

        if "GET" in packet:
            self.debug("sending the file")
            print("sending the file")
            await ftp.send_file("/sd/tree.png")
        print("done enqueueing")
        while outbox.qsize() != 0:
            self.debug(outbox.qsize())
            yield
        else:
            self.debug("TEST PASSED")
        yield