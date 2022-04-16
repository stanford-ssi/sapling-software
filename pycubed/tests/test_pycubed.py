# this file runs the tests on a host computer
import os
import sys
import shutil
import logging
import pathlib
import re
from collections import namedtuple

import serial
import pytest

LOGGER = logging.getLogger(__name__)

ignore_list = [
    "Light Sensor"
]

class PyCubed:

    def __init__(self, drive, device):
        self.drive = drive
        self.connection = serial.Serial(str(device), timeout = 5)

    def readlines(self):
        yield self.connection.readline().decode('ascii')

    def load_code(self, code_location):
        for file in os.listdir(self.drive):
            if os.path.isdir(file):
                os.rmdir(file)
            else:
                os.remove(file)
        shutil.copy2(code_location, self.drive)
        pycubed.connection.read()
        self.reset()

    def reset(self):
        self.connection.write(b'\x04')

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
        r = re.compile("tty\.usbmodem.*")
        potential_devices = list(filter(r.match, devices))
        if len(potential_devices):
            print(str(dev_folder / potential_devices[0]))
            try:
                pycubed = PyCubed(mount_point, dev_folder / potential_devices[0])
                return pycubed
            except serial.serialutil.SerialException as e:
                LOGGER.log(e)
                pytest.xfail(f"Could not connect to PyCubed: {e}")
        else:
            LOGGER.log(f"more than one device discovered mounted to host: \
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
    os.rmdir("tmp")

#TODO figure out a way to discover these test folders
@pytest.fixture(params=["test_file_utils", "test_ftp"])
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
    pycubed_src = cwd.parent / "src"

    print(pycubed_src)
    print(staging_area)
    shutil.copytree(pycubed_src, staging_area, dirs_exist_ok=True)

    # copy files to pycubed
    if os.path.isdir(cwd / path_to_test):
        shutil.copytree(cwd / path_to_test, staging_area, dirs_exist_ok=True)

    # copy files to pycubed
    pycubed.load_code(staging_area)

    # check the hardware config and (skip tests) that won't work
    for line in pycubed.readlines():
        LOGGER.log(line)
        if line == 'Finished initializing PyCubed Hardware': #TODO make less jank
            break
        if "ERROR" in line:
            for ignore in ignore_list: #TODO ignore by test
                if ignore not in line:
                    pytest.xfail(line)

    # log output of test
    last_line = ""
    for line in pycubed.readlines():
        LOGGER.log(line)
        if "TEST PASSED" in line:
            break
        elif "ERROR" in line:
            test.xfail(line)
        last_line = line
        #TODO find a way to check that each individual assert passes, with some
        #sort of test definition file
    assert("TEST PASSED" in last_line)
