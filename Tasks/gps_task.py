# check for GPS information

from Tasks.template_task import Task
import time

class task(Task):
    priority = 6
    frequency = 1/20 # once every 20s
    name='GPS'
    color = 'blue'

    async def main_task(self):
        GPS_ANTENNA = False
        # Turn GPS_ANTENNA to True if connected, otherwise keep false to protect
        # chip from reflectance
        if GPS_ANTENNA:
            self.debug('GPS attempt, trying to get fix...')
            last_print = time.monotonic()
            while True:
                self.cubesat.gps.update()

                current = time.monotonic()
                if current - last_print >= 1.0:
                    last_print = current
                    if not self.cubesat.gps.has_fix:
                        # Try again if we don't have a fix yet.
                        self.debug("Waiting for fix...be patient!")
                        continue

                    # We have a fix! (gps.has_fix is true)
                    # Print out details about the fix like location, date, etc.
                    self.debug(
                        "Fix timestamp: {}/{}/{} {:02}:{:02}:{:02}".format(
                            self.cubesat.gps.timestamp_utc.tm_mon,  # Grab parts of the time from the
                            self.cubesat.gps.timestamp_utc.tm_mday,  # struct_time object that holds
                            self.cubesat.gps.timestamp_utc.tm_year,  # the fix time.  Note you might
                            self.cubesat.gps.timestamp_utc.tm_hour,  # not get all data like year, day,
                            self.cubesat.gps.timestamp_utc.tm_min,  # month!
                            self.cubesat.gps.timestamp_utc.tm_sec,
                        ), 2
                    )
                    self.debug("Latitude: {0:.6f} degrees".format(self.cubesat.gps.latitude),2)
                    self.debug("Longitude: {0:.6f} degrees".format(self.cubesat.gps.longitude), 2)
                    self.debug("Fix quality: {}".format(self.cubesat.gps.fix_quality), 2)
        else:
            self.debug('GPS antenna set to false, to use GPS task turn variable to true!')
