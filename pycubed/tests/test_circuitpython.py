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
import json

import serial
import pytest
import adafruit_board_toolkit.circuitpython_serial

LOGGER = logging.getLogger(__name__)

class Board:
    """A CircuitPython board abstraction.
    """

    def __init__(self, mount_point, repl_port, data_port, **kwargs):
        """Check whether the board is mounted correctly and configuration is 
        valid, and connects to its repl and data ports.

        Args:
            mount_point (str, pathlike): path to the mount point of the board.
                /Volumes on MacOS.
            device (str, pathlike): path to the repl serial port 
        """
        self.repl_conn = serial.Serial(str(repl_port), timeout = 10)
        self.data_conn = serial.Serial(str(data_port), timeout = 10)
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
        self.drive = pathlib.Path(mount_point) / self.drive_name
        if not os.path.isdir(self.drive):
            pytest.xfail(f"Board not mounted in expected location {self.drive}")
        LOGGER.debug(self.__dict__)

    def readline(self):
        """read a line, decode as ascii, and strip the newline character

        Returns:
            str: a chunk of data
        """
        return self.repl_conn.readline().decode('ascii').strip('\n')

    def load_code(self, code_location):
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
            # copy src files to target
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
        try:
            shutil.copytree(self.entry_point, self.drive)
        except OSError as e: # shutil has a lot of OSErrors [errno22]
            LOGGER.debug(e)

        self.reset()

    def reset(self):
        """Reset the target device
        """
        self.repl_conn.write(b'\x03') # ctrl-c
        self.repl_conn.write(b'\x04') # ctrl-d


@pytest.fixture
def board():
    """Fixture that instantiates a Board, failing if no board is discovered or
    if the host is unable to establish a connection to the target.

    Returns:
        Board: a board object
    """
    if sys.platform == 'darwin':
        if os.path.isdir("/Volumes"):
            mount_point = "/Volumes"
    else:
        pytest.xfail("Tests do not yet work on platforms other than MacOS")
    repl_ports = adafruit_board_toolkit.circuitpython_serial.repl_comports()
    data_ports = adafruit_board_toolkit.circuitpython_serial.data_comports()
    
    with open("board.json") as f:
        board_config = json.load(f)
    if repl_ports and data_ports:
        if len(repl_ports) > 1:
            LOGGER.info(f"More than one target discovered -- repl: \
                {[port.device for port in repl_ports]} \
                data: {[port.device for port in data_ports]}")
        try:
            LOGGER.info(f"Connecting to repl: {repl_ports[0].device} \
                and data: {data_ports[0].device}")
            connected_board = Board(mount_point, repl_ports[0].device, 
                data_ports[0].device, **board_config)
            return connected_board
        except serial.serialutil.SerialException as e:
            LOGGER.error(e)
            pytest.xfail(f"Unable to connect to board: {e}")
    else:
        LOGGER.error(f"No boards discovered: {repl_ports}")

@pytest.fixture
def change_test_dir(request):
    """Chnges to directory of current test, and return to pytest invocation
    directory after the test completes.
    """
    os.chdir(request.fspath.dirname)
    yield
    os.chdir(request.config.invocation_dir)

#TODO figure out a way to discover these test folders
@pytest.fixture(params=["file_utils"]) #"ftp", "file_utils"
def name_of_test(change_test_dir, request):
    """Parametrized fixture that returns the name of a test

    Args:
        change_test_dir (fixture): fixture
        request (request): pytest fixture parametrization object

    Returns:
        str: name of test
    """
    filename = request.param
    return filename

def test(name_of_test, board):
    """Pytest test. Copies files to the target, and runs tests either using a
    custom test runner defined in the `name_of_test` folder, or using a generic
    runner defined in `runner.py`

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