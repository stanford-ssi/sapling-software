# check for low battery condition

from Tasks.template_task import Task
import time

class task(Task):
    priority = 3
    frequency = 1/10 # once every 10s
    name='ads'
    color = 'blue'

    async def main_task(self):
        pass
        # read in data from cubesat.gps
        # run through filter
        # write to cubesat.position and cubesat.velocity