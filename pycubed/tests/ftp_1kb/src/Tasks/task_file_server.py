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
        
        while True:
            packet = await inbox.get()
            #print(packet)
            if packet:
                break
            yield

        if "GET" in packet:
            self.debug("sending the file")
            print("sending the file")
            await ftp.send_file("/sd/1kb.png")
        print("done enqueueing")
        while outbox.qsize() != 0:
            self.debug(outbox.qsize())
            yield
        else:
            self.debug("TEST PASSED")
        yield