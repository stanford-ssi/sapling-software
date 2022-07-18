from Tasks.template_task import Task
from protocol_shared import aptp

class task(Task):
    priority = 1
    frequency = 10 # once every 1s
    name = 'receive task'
    color = 'yellow'

    schedule_later = True

    async def main_task(self):
        await aptp.receive()