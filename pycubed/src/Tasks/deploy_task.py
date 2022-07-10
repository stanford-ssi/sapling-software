# deploy antenna

from Tasks.template_task import Task
import time

class task(Task):
    priority = 3
    frequency = 1/10 # once every 10s, will only complete once
    name='deploy'
    color = 'red'
    
    timeout=5 # 30 sec

    async def main_task(self):
       
        _timer=time.monotonic() + self.timeout
        while time.monotonic() < _timer:
            yield
        if not self.cubesat.f_deployed:
            self.cubesat.burn(dutycycle=0.05, duration=3)
        self.cubesat.scheduled_tasks['deploy'].stop()
