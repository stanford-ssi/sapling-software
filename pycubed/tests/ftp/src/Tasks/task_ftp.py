from Tasks.template_task import Task
import time
from tasko.loop import _yield_once
from protocol_shared import f

NEED_TO_READ_PACKET = True

class task(Task):
    priority = 2
    frequency = 10 # once every 1s
    name = 'ftp task'
    color = 'red'

    schedule_later = True

    async def main_task(self):
        global WAITING_FOR_REQUEST
        
        if WAITING_FOR_REQUEST:
            packet = await f.inbox.pop()
            if "GET" in packet:
                self.debug("sending the file")
                await f.send_file("/sd/hello.txt")
                print(f.outbox)
                WAITING_FOR_REQUEST = False
            yield
        else:
            self.debug("else")
            _yield_once()
            