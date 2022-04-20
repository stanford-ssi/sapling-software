from Tasks.template_task import Task
import time
from protocol_shared import f
from tasko.loop import _yield_once

NEED_TO_SEND_PACKET = True

class task(Task):
    priority = 1
    frequency = 10 # once every 1s
    name = 'task a'
    color = 'blue'

    schedule_later = True

    async def main_task(self):
        global NEED_TO_SEND_PACKET

        if NEED_TO_SEND_PACKET:
            self.debug("waiting to recieve packet")
            packet = await f.receive_packet()
            self.debug(f"recieved packet: {packet}")
            self.debug(f"sending packets!")
            while f.outbox.empty():
                yield
            sent = await f.send()
            NEED_TO_SEND_PACKET = not sent
            self.debug(f"TEST PASSED: {packet}")
            yield
        else:
            self.debug("else")
            pass