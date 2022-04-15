from pycubed import cubesat
import file_utils
import os

test_file = "/sd/LOCKING_TEST_FILE"
lock_file = test_file + ".lock"
if file_utils.exists(test_file):
    os.remove(test_file)
if file_utils.exists(lock_file):
    os.remove(lock_file)