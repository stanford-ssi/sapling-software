# check for low battery condition

from Tasks.template_task import Task
import time

class task(Task):
    priority = 3
    frequency = 1/10 # once every 10s
    name='vbatt'
    color = 'orange'

    async def main_task(self):
        self.debug('Power Readings:')
        self.debug('       Battery Voltage: {:.1f}V (Threashold of {:.1f}V)'.format(self.cubesat.battery_voltage,self.cubesat.vlowbatt),2)
        # self.debug('  Battery Current Draw: {:.1f}mA (Not accurate if powered by USB)'.format(self.cubesat.current_draw),2)
        self.debug('Solar Charging Current: {:.1f}mA'.format(self.cubesat.charge_current()),2)
        self.debug('          USB Charging: {}'.format(self.cubesat.charge_batteries),2)

        #TODO: add print statement with USB charging current if usb charging on
