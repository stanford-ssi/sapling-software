from Tasks.template_task import Task
import time
from protocol_shared import f
inbox = f.inbox
outbox = f.outbox

NEED_TO_READ_PACKET = True

class task(Task):
    priority = 1
    frequency = 10 # once every 1s
    name = 'task a'
    color = 'blue'

    schedule_later = True

    async def main_task(self):
        global NEED_TO_READ_PACKET
        
        if NEED_TO_READ_PACKET:
            packet = await inbox.pop()
            assert("hello" in packet)
            self.debug(f"ASSERT PASSED: recieved packet: {packet}")
            packet_to_send = "hello from pycubed"
            outbox.pushleft(packet_to_send)
            self.debug(f"TEST PASSED: {packet}")
            NEED_TO_READ_PACKET = False
            yield
        else:
            pass