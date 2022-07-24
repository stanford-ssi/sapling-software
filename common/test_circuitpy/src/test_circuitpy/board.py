import asyncio
import os
import pathlib
import time
import logging

import shutil

import serial_asyncio
import adafruit_board_toolkit.circuitpython_serial

LOGGER = logging.getLogger(__name__)

TEST_DIR = pathlib.Path(__file__).parent.resolve()
PYCUBED_DIR = TEST_DIR.parent.resolve() # TODO fix this

class aobject(object):
    """Inheriting this class allows you to define an async __init__.

    So you can create objects by doing something like `await MyClass(params)`

    from: https://stackoverflow.com/a/45364670
    """
    async def __new__(cls, *a, **kw):
        instance = super().__new__(cls)
        await instance.__init__(*a, **kw)
        return instance

    async def __init__(self):
        pass


class Board(aobject):
    """A CircuitPython board abstraction.
    """

    async def __init__(self, mount_point, repl_port, board_src_dir, **kwargs):
        """Check whether the board is mounted correctly and configuration is 
        valid, and connects to its repl and data ports.

        Args:
            mount_point (str, pathlike): path to the mount point of the board.
                /Volumes on MacOS.
            device (str, pathlike): path to the repl serial port 
        """
        self.board_src_dir = board_src_dir
        self.common_src_dir = PYCUBED_DIR / "src"
        self.__dict__.update(kwargs)
        LOGGER.debug(self.__dict__)

        # check validity of args and install defaults
        allowed_args = ('drive_name', 'ignore_patterns', 'include_files', 'entry_point', "ignore_errors")
        default_values = {
            'drive_name': 'CIRCUITPY',
            'ignore_patterns': None, 
            'include_files': None, 
            'entry_point': None,
            "ignore_errors": []
        } 
        self.__dict__.update(default_values)
        if set(kwargs.keys()).issubset(allowed_args):
            self.__dict__.update(kwargs)
        else:
            unallowed_args = set(kwargs.keys()).difference(allowed_args)

        # find CIRCUITPY drive
        self.drive = pathlib.Path(mount_point) / self.drive_name
        if not os.path.isdir(self.drive):
            LOGGER.warning(f"Board not mounted in expected location {self.drive}, timing out for 3s")
            await asyncio.sleep(3)
        if not os.path.isdir(self.drive):
            LOGGER.error(f"Board not mounted in expected location {self.drive}")

        # connect to REPL for debug and command info
        self.debug_stream, self.command_stream = await serial_asyncio.open_serial_connection(url=str(repl_port), baudrate=115200)
            
        # check whether the data connection is enabled
        data_ports = adafruit_board_toolkit.circuitpython_serial.data_comports()
        if not len(data_ports):
            self.load_entry_point()
            LOGGER.info("HEY THERE! YOU! PRESS THE RESET BUTTON ON YOUR BOARD")
            time.sleep(5) # wait for board to boot
            data_ports = adafruit_board_toolkit.circuitpython_serial.data_comports()
        
        if not len(data_ports):
            LOGGER.error("UNABLE TO ACTIVATE SERIAL DATA PORT, DID YOU CLICK THE BUTTON WHEN PROMPTED?")
        
        # connect to data port
        self.data_receive_stream, self.data_send_stream = await serial_asyncio.open_serial_connection(url=str(data_ports[0].device), baudrate=115200)
        

    async def readline(self):
        """read a line, decode as ascii, and strip the newline character

        Returns:
            str: a chunk of data
        """
        data = await self.debug_stream.readline()
        return data.decode('ascii').strip('\n')

    def erase_circuitpy_drive(self):
        for file in os.listdir(self.drive):
            if file == ".Trashes":
                continue # jank
            elif "._" in file:
                continue
            elif os.path.isdir(self.drive / file):
                shutil.rmtree(self.drive / file)
            else:
                os.remove(self.drive / file)

    def load_entry_point(self):
        # copy entry point
        try:
            shutil.copytree(self.entry_point, self.drive, dirs_exist_ok=True)
        except OSError as e: # shutil has a lot of OSErrors [errno22]
            LOGGER.debug(e)

    def load_src(self):
        try:
            # copy src files to target
            if self.common_src_dir:
                ignore_patterns = ["__pychache__"]
                if self.ignore_patterns:
                    ignore_patterns.extend(self.ignore_patterns)
                
                if self.include_files:
                    for file in self.include_files:
                        file_common = self.common_src_dir / file
                        file_board_specific = self.board_src_dir / file
                        target = self.drive / file
                        if not os.path.exists(target.parent):
                            os.mkdir(target.parent)
                        
                        # files are overriden here
                        if file_board_specific.exists():
                            shutil.copy(file_board_specific, target)
                            continue
                        elif file_common.exists():
                            shutil.copy(file_common, target)
            
                try:
                    shutil.copytree(self.common_src_dir, self.drive, ignore = shutil.ignore_patterns(*ignore_patterns), dirs_exist_ok=True)
                except OSError as e: # shutil has a lot of OSErrors [errno22]
                    LOGGER.debug(e)
                shutil.copytree(self.board_src_dir, self.drive, ignore = shutil.ignore_patterns(*ignore_patterns), dirs_exist_ok=True)
        
                LOGGER.info("done")

        except OSError as e: # shutil has a lot of OSErrors [errno22]
            LOGGER.debug(e)

    def load_test_code(self, code_location):
        """Deletes all files on the target decide, then copies code from the 
        host computer to the target CircuitPython device. Copies:
            files from self.source, ignoring self.ignore_patterns, and including
                self.include_files
            all files from code_location
            all files from self.entry_point
        Then, resets the target device.
        
        Args:
            code_location (str, pathlike): path to location of code on the
                source computer that will be copied to the CircuitPython device
        """ 
        self.erase_circuitpy_drive()
        self.load_src()

        # copy test code
        try:
            shutil.copytree(code_location, self.drive, dirs_exist_ok=True)
        except OSError as e: # shutil has a lot of OSErrors [errno22]
            LOGGER.debug(e)

        # copy entry point
        self.load_entry_point()

        self.reset()

    def reset(self):
        """Reset the target device, and enable data line
        """
        self.command_stream.write(b'\x03') # ctrl-c
        self.command_stream.write(b'\x04') # ctrl-d
