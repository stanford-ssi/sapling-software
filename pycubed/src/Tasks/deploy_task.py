# check for low battery condition

from Tasks.template_task import Task
import time

class task(Task):
    priority = 3
    frequency = 1/10 # once every 10s, will only complete once
    name='deploy'
    color = 'red'

    timeout=30 # 30 sec

    async def main_task(self):
       
        _timer=time.monotonic() + self.timeout
        while time.monotonic() < _timer:
            yield
        self.cubesat.burn(0.1)
        self.cubesat.scheduled_tasks['deploy'].stop()
