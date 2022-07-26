# deploy antenna

from Tasks.template_task import Task
import time

class task(Task):
    priority = 3
    frequency = 1/10 # once every 10s, will only complete once
    name='deploy'
    color = 'red'
    
    timeout=30

    async def main_task(self):
       
        _timer=time.monotonic() + self.timeout
        while time.monotonic() < _timer:
            yield
        if not self.cubesat.f_deployed:
            self.cubesat.burn(dutycycle=0.09, duration=1, freq=1500)
        self.cubesat.scheduled_tasks['deploy'].stop()
