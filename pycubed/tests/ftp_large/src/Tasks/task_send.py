from Tasks.template_task import Task
from protocol_shared import aptp

class task(Task):
    priority = 1
    frequency = 10 # once every 1s
    name = 'send task'
    color = 'green'

    schedule_later = True

    async def main_task(self):
        await aptp.send()