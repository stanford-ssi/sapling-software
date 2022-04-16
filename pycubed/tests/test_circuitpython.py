"""
`test_circuitpython`
====================================================

CircuitPython test harness that runs on a host computer

* Author(s): Flynn Dreilinger

Implementation Notes
--------------------

"""
import os
import sys
import shutil
import logging
import pathlib
import re

import serial
import pytest

LOGGER = logging.getLogger(__name__)

ignore_list = [
    "Light Sensor"
]

class PyCubed:

    def __init__(self, drive, device):
        self.drive = drive
        self.connection = serial.Serial(str(device), timeout = 100)

    def readlines(self):
        line = self.connection.readline().decode('ascii')
        print(line)
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
            shutil.copytree(code_location, self.drive, ignore = shutil.ignore_patterns("__pychache__"), dirs_exist_ok=True)
        except OSError as e:
            # LOGGER.info(e)
            pass
        self.reset()

    def reset(self):
        self.connection.write(b'\x03') # ctrl-c
        self.connection.write(b'\x04') # ctrl-d

@pytest.fixture
def pycubed_location():
    if sys.platform == 'darwin':
        return ("/Volumes/PYCUBED", "/dev")
    else:
        pytest.xfail("Tests not tested on platforms other than MacOS")

@pytest.fixture
def pycubed(pycubed_location):
    mount_point = pathlib.Path(pycubed_location[0])
    dev_folder = pathlib.Path(pycubed_location[1])
    if os.path.isdir(dev_folder):
        devices = os.listdir(dev_folder)
        r = re.compile("tty.usbmodem.*")
        potential_devices = list(filter(r.match, devices))
        if len(potential_devices):
            print(str(dev_folder / potential_devices[0]))
            try:
                pycubed = PyCubed(mount_point, dev_folder / potential_devices[0])
                return pycubed
            except serial.serialutil.SerialException as e:
                LOGGER.error(e)
                pytest.xfail(f"Could not connect to PyCubed: {e}")
        else:
            LOGGER.error(f"more than one device discovered mounted to host: \
                {potential_devices}")
    else:
        pytest.xfail("PyCubed drive not mounted")

@pytest.fixture
def change_test_dir(request):
    """chdir to directory of current test
    """
    os.chdir(request.fspath.dirname)
    yield
    os.chdir(request.config.invocation_dir)

@pytest.fixture()
def staging_area(change_test_dir):
    os.mkdir("tmp")
    yield pathlib.Path.cwd() / "tmp"
    shutil.rmtree("tmp")

#TODO figure out a way to discover these test folders
@pytest.fixture(params=["file_utils"]) #"ftp"
def path_to_test(request):
    filename = request.param
    return filename

def test(staging_area, path_to_test, pycubed):
    """This is where tests are run

    Args:
        setup_tests (str): path to the tmp folder
        pycubed_test (str): path to the files that will be used for the test
    """
    cwd = pathlib.Path.cwd()
    pycubed_src = cwd.parent / "src" #/ "lib"
    pycubed_temp_task = cwd.parent / "src" / "Tasks" / "template_task.py"
    entry_point = cwd / "entry_point.py"

    # copy src files to staging area
    shutil.copytree(pycubed_src, staging_area, ignore = shutil.ignore_patterns("Tasks"), dirs_exist_ok=True)
    shutil.copy(entry_point, staging_area / "code.py")
    os.mkdir(staging_area / "Tasks")
    shutil.copy(pycubed_temp_task, staging_area / "Tasks" / "template_task.py")

    # copy test files to staging area
    if os.path.isdir(cwd / path_to_test):
        shutil.copytree(cwd / path_to_test, staging_area, dirs_exist_ok=True)

    # copy files to pycubed
    pycubed.load_code(staging_area)

    # check the hardware config and (skip tests) that won't work
    while True:
        line = pycubed.connection.readline().decode('ascii')
        LOGGER.info(line)
        if "TEST PASSED" in line:
            LOGGER.info(line)
            break
        if "ERROR" in line:
            LOGGER.error(line)
            for ignore in ignore_list: # TODO ignore by test
                if ignore not in line:
                    pytest.xfail(line)
