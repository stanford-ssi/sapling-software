from Tasks.template_task import Task
import time
from protocol_shared import aptp
from tasko.loop import _yield_once

NEED_TO_SEND_PACKET = True

class task(Task):
    priority = 1
    frequency = 10 # once every 1s
    name = 'test task'
    color = 'red'

    schedule_later = True

    async def main_task(self):
        global NEED_TO_SEND_PACKET

        if NEED_TO_SEND_PACKET:
            self.debug("Receiving...")
            for i in range(100):
                packet = await aptp._receive_packet()
                if int(packet) != i:
                    self.debug(f"Expecting packet {i}, received {packet}")
            self.debug(f"Received 100 sequenced packets from host")
            self.debug(f"Sending packets!")
            for i in range(100):
                sent = await aptp._send_packet(f"{i}")
                if not sent:
                    self.debug(f"Did not receive an ACK on packet {i}")
            self.debug(f"Sent 100 ACKs!")
            NEED_TO_SEND_PACKET = False
            self.debug(f"TEST PASSED: {packet}")
            yield
        else:
            self.debug("else")
            pass