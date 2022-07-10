"""
`test_circuitpython`
====================================================

CircuitPython test harness that runs on a host computer

* Author(s): Flynn Dreilinger

Implementation Notes
--------------------

"""
import asyncio
import os
import sys

import logging
import pathlib
import json

import pytest
import pytest_asyncio
import adafruit_board_toolkit.circuitpython_serial

from tests.circuitpython_board import Board

LOGGER = logging.getLogger(__name__)
TEST_DIR = pathlib.Path(__file__).parent.resolve()
TESTS = [
    dirent 
    for dirent 
    in TEST_DIR.iterdir() 
    if dirent.is_dir()
]

@pytest_asyncio.fixture
async def board():
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
    
    with open("board.json") as f:
        board_config = json.load(f)
    if repl_ports:
        if len(repl_ports) > 1:
            LOGGER.info(f"More than one target discovered -- repl: \
                {[port.device for port in repl_ports]}")
        try:
            LOGGER.info(f"Connecting to board with repl at {repl_ports[0].device}")
            connected_board = await Board(mount_point, repl_ports[0].device, 
                **board_config)
            if not connected_board:
                LOGGER.warning("Unable to connect to board, timing out for 3s")
                await asyncio.sleep(3)
                connected_board = await Board(mount_point, repl_ports[0].device, 
                    **board_config)
            return connected_board
        except Exception as e:
            LOGGER.error(e)
            pytest.xfail(f"Unable to connect to board: {e}")
    else:
        LOGGER.error(f"No boards discovered: {repl_ports}")

@pytest.fixture
def change_test_dir(request):
    """Changes to directory of current test, and return to pytest invocation
    directory after the test completes.
    """
    os.chdir(request.fspath.dirname)
    yield
    os.chdir(request.config.invocation_dir)

@pytest.fixture(
    params=TESTS,
    ids=[test.name for test in TESTS]
)
def test_dir(change_test_dir, request):
    """Parametrized fixture that returns the name of a test

    Args:
        change_test_dir (fixture): fixture
        request (request): pytest fixture parametrization object

    Returns:
        str: name of test
    """
    filename = request.param
    return filename

@pytest.mark.asyncio # tests do not run concurrently with each other
async def test(test_dir, board):
    """Pytest test. Copies files to the target, and runs tests either using a
    custom test runner defined in the `test_dir` folder, or using a generic
    runner defined in `runner.py`

    Args:
        test_dir (str): path to the files that will be used for the test
        board (Board): Board object that provides mount point and connection to 
        the board
    """
    cwd = pathlib.Path.cwd()
    test_name = test_dir.name
    # copy test files to board
    if os.path.isdir(cwd / test_dir / "src"):
        board.load_test_code(cwd / test_dir / "src")

    # check if test has a custom runner
    if os.path.isfile(cwd / test_dir / "runner.py"):
        exec(f"from tests.{test_name}.runner import TestRunner", globals())
        t = TestRunner(board, LOGGER)

    # default runner
    else:
        from tests.runner import BaseRunner
        t = BaseRunner(board, LOGGER)

    print(type(t))
    await t.run()
