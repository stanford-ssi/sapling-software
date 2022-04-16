"""
`test_circuitpython`
====================================================

CircuitPython test harness that runs on a host computer

* Author(s): Flynn Dreilinger

Implementation Notes
--------------------

"""
from importlib.metadata import entry_points
import os
import sys
import shutil
import logging
import pathlib
import re
import json

import serial
import pytest

LOGGER = logging.getLogger(__name__)

class Board:

    def __init__(self, mount_point, device, **kwargs):
        self.connection = serial.Serial(str(device), timeout = 100)
        self.__dict__.update(kwargs)
        allowed_args = ('drive_name', 'src_dir', 'ignore_patterns', 'include_files', 'entry_point', "ignore_errors")
        default_values = {
            'drive_name': 'CIRCUITPY',
            'src_dir': '../src', 
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
            pytest.xfail(f"Unsupported argument(s) passed to Board:\n{unallowed_args}")
        self.drive = mount_point / self.drive_name
        if not os.path.isdir(self.drive):
            pytest.xfail(f"Board not mounted in expected location {self.drive}")
        LOGGER.debug(self.__dict__)

    def readline(self):
        return self.connection.readline().decode('ascii').strip('\n')

    def readlines(self):
        line = self.connection.readline().decode('ascii')
        yield line

    def load_code(self, code_location): 
        for file in os.listdir(self.drive):
            if file == ".Trashes":
                continue # jank
            elif "._" in file:
                continue
            elif os.path.isdir(self.drive / file):
                shutil.rmtree(self.drive / file)
            else:
                os.remove(self.drive / file)
        try:
            # copy src files to staging area
            if self.src_dir:
                ignore_patterns = ["__pychache__"]
                if self.ignore_patterns:
                    ignore_patterns.extend(self.ignore_patterns)
                
                if self.include_files:
                    for file in self.include_files:
                        source = pathlib.Path(self.src_dir) / file
                        target = self.drive / file
                        if not os.path.exists(target.parent):
                            os.mkdir(target.parent)
                        shutil.copy(source, target)
                shutil.copytree(self.src_dir, self.drive, ignore = shutil.ignore_patterns(*ignore_patterns), dirs_exist_ok=True)

        except OSError as e: # shutil has a lot of OSErrors [errno22]
            LOGGER.debug(e)

        # copy test code
        try:
            shutil.copytree(code_location, self.drive, dirs_exist_ok=True)
        except OSError as e: # shutil has a lot of OSErrors [errno22]
            LOGGER.debug(e)

        # copy entry point
        if self.entry_point:
            shutil.copy(self.entry_point, self.drive / "code.py")

        self.reset()

    def reset(self):
        self.connection.write(b'\x03') # ctrl-c
        self.connection.write(b'\x04') # ctrl-d

@pytest.fixture
def platform_specific_setup():
    if sys.platform == 'darwin':
        if os.path.isdir("/Volumes"):
            return ("/Volumes", "/dev")
    else:
        pytest.xfail("Tests do not yet work on platforms other than MacOS")

@pytest.fixture
def board(platform_specific_setup):
    mount_point = pathlib.Path(platform_specific_setup[0])
    dev_folder = pathlib.Path(platform_specific_setup[1])
    
    with open("board.json") as f:
        board_config = json.load(f)
    devices = os.listdir(dev_folder)
    r = re.compile("tty.usbmodem.*")
    potential_devices = list(filter(r.match, devices))
    if potential_devices:
        if len(potential_devices) > 1:
            LOGGER.info(f"More than one board discovered: {potential_devices}")
        try:
            LOGGER.info(f"Connecting to \
                {dev_folder / potential_devices[0]}")
            board = Board(mount_point, dev_folder / potential_devices[0], **board_config)
            return board
        except serial.serialutil.SerialException as e:
            LOGGER.error(e)
            pytest.xfail(f"Unable to connect to board: {e}")
    else:
        LOGGER.error(f"No boards discovered: {potential_devices}")

@pytest.fixture
def change_test_dir(request):
    """chdir to directory of current test
    """
    os.chdir(request.fspath.dirname)
    yield
    os.chdir(request.config.invocation_dir)

#TODO figure out a way to discover these test folders
@pytest.fixture(params=["file_utils"]) #"ftp"
def name_of_test(change_test_dir, request):
    filename = request.param
    return filename

def test(name_of_test, board):
    """This is where tests are run

    Args:
        name_of_test (str): path to the files that will be used for the test
        board (Board): Board object that provides mount point and connection to 
        the board
    """
    cwd = pathlib.Path.cwd()

    # copy test files to board
    if os.path.isdir(cwd / name_of_test / "src"):
        board.load_code(cwd / name_of_test / "src")

    # check if test has a custom runner
    if os.path.isfile(cwd / name_of_test / "runner.py"):
        exec(f"from tests.{name_of_test}.runner import TestRunner", globals())
        t = TestRunner(board, LOGGER)

    # default runner
    else:
        from tests.runner import BaseRunner
        t = BaseRunner(board, LOGGER)

    t.run()