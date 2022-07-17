from Tasks.template_task import Task
import time
from protocol_shared import ptp
from tasko.loop import _yield_once

NEED_TO_SEND_PACKET = True

class task(Task):
    priority = 1
    frequency = 10 # once every 1s
    name = 'receive task'
    color = 'blue'

    schedule_later = True

    async def main_task(self):
        await ptp.receive()