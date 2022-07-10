from Tasks.template_task import Task
import time
import os
import digitalio
from tasko.loop import _yield_once
from ulab import numpy as np
import traceback

TEST_COMPLETE = False

class task(Task):
    priority = 1
    frequency = 10 # once every 1s
    name = 'task a'
    color = 'blue'

    schedule_later = True

    async def main_task(self):
        global TEST_COMPLETE

        if not TEST_COMPLETE:
            self.debug("waiting to recieve packet")
            overall_success = True
            # IMU
            imu_success = True
            self.debug(f"Testing whether IMU is returning data")
            a = self.cubesat.acceleration
            g = self.cubesat.gyro
            m = self.cubesat.magnetic
            imu_success = imu_success and np.linalg.norm(a) > 0
            imu_success = imu_success and np.linalg.norm(g) > 0
            imu_success = imu_success and np.linalg.norm(m) > 0
            self.debug(f"[IMU]: {imu_success}")

            # test whether power monitor is responsive
            pwr_monitor_success = self.cubesat.pwr.status == 0 # TODO figure out what the status should actually be
            self.debug(f"[Power Monitor]: {pwr_monitor_success}") 

            # test whether relay works (you need to listen to the board to hear a click)
            self.cubesat._relayA.drive_mode=digitalio.DriveMode.PUSH_PULL
            self.cubesat._relayA.value = 1
            time.sleep(0.5)
            self.cubesat._relayA.value = 0
            self.cubesat._relayA.drive_mode=digitalio.DriveMode.OPEN_DRAIN

            # test whether Sun Sensors are returning data
            light_sensor_success = True
            lux = await self.cubesat.lux
            for i, reading in enumerate(lux):
                sensor = self.cubesat.light_sensor_ordered[i]
                valid_reading = reading and reading > 0
                light_sensor_success = light_sensor_success and valid_reading
                self.debug(f"[Light Sensor][{sensor}]: {valid_reading}")
            self.debug(f"[Light Sensor]: {light_sensor_success}")

            # test whether Coral can boot and respond to simple commands
            self.cubesat.coral.turn_on()
            coral_success = self.cubesat.coral.ping()
            self.debug(f"[CORAL]: {coral_success}" )

            # test whether GPS is responsive
            gps_success = self.cubesat.gps.update()
            self.debug(f"[GPS]: {gps_success}")

            # test whether Radio is responsive and configured for LoRa
            radio_success = self.cubesat.radio1.long_range_mode == 1
            self.debug(f"[Radio]: {radio_success}")

            # test writing/reading from SD card
            sd_success = True
            filename = '/sd/test_rw.txt'
            test_string = "DROFNATS"
            with open(filename,'w') as f:
                f.write(test_string)
            with open(filename,'r') as f:
                sd_success = f.readline() == test_string
                self.debug(f"[SD]: {sd_success}")
            os.remove(filename)

            TEST_COMPLETE = True
            overall_success = (
                imu_success 
                and pwr_monitor_success
                and light_sensor_success
                and coral_success
                and gps_success
                and radio_success
                and sd_success
            )
            self.debug(f"[Satellite Integrity]: {overall_success}")
            self.debug(f"COMPLETE")
            yield
        else:
            self.debug("else")
            pass