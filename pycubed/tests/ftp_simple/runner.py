import asyncio
import pathlib
import filecmp

import pytest 

from sapling.utils.ptp import AsyncPacketTransferProtocol
from sapling.utils.ftp import FileTransferProtocol

from tests.runner import BaseRunner


TEST_DIR = pathlib.Path(__file__).parent.resolve()


class TestRunner(BaseRunner):

    def __init__(self, *args, **kwargs):
        super(TestRunner, self).__init__(*args, **kwargs)
        self.done = False
        self.ptp = AsyncPacketTransferProtocol(self.board.data_receive_stream, self.board.data_send_stream)
        self.ftp = FileTransferProtocol(self.ptp)

    # repl used for debug info and test status
    async def repl(self):
        while True:
            line = await self.board.readline()
            if '----------------------------------------' in line:
                self.test_started = True
            if self.test_started:
                self.LOGGER.info(line)
                if "Running..." in line:
                    self.tasks_running = True
                if "TEST PASSED" in line:
                    print("hello?????")
                    await asyncio.sleep(1) # make sure other command tasks can print output
                    self.done = True
                    return
                if "ERROR" in line:
                    if self.board.ignore_errors:
                        for error in self.board.ignore_errors: # TODO ignore by test
                            if error in line:
                                self.LOGGER.debug(line) 
                                break # only need to see one error
                        else: # non-ignored error has been seen
                            self.LOGGER.error(line) 
                            pytest.xfail(line)
                    else:
                        self.LOGGER.error(line) 
                        pytest.xfail(line)
                    
    # send a packet, wait for response once
    async def send_and_recieve_packets(self):
        test_filename = "hello.txt"
        while not self.tasks_running:
            await asyncio.sleep(0.1)
        self.debug("Requesting file from PyCubed")
        await self.ftp.request_file("hello.txt", TEST_DIR / test_filename)
        self.debug("Received file from PyCubed")
        with open(TEST_DIR / test_filename) as f:
            f.readlines()

    async def write(self):
        while not self.tasks_running:
            await asyncio.sleep(0.1)
        self.debug("starting writer")
        while True:
            await self.ptp.send()

    
    async def read(self):
        while not self.tasks_running:
            await asyncio.sleep(0.1)
        self.debug("starting reader")
        await self.ptp.receive()

    async def monitor(self, tasks):
        # monitor the state of tasks and cancel some
        while not all(t.done() for t in tasks):
            for t in tasks:
                if not t.done() and self.done == True:
                    t.cancel()
            # give the tasks some time to make progress
            await asyncio.sleep(1)

    async def run(self):
        """Runs a test. Logs output before the entry point of main.py on debug,
        and output after on info. Fails current pytest if `ERROR` is present 
        in output, and passes (does not call pytest.xfail) if `TEST PASSED` is
        present.
        """
        self.test_started = False
        self.tasks_running = False
        tasks = [
            asyncio.create_task(self.repl()),
            asyncio.create_task(self.write()), 
            asyncio.create_task(self.read()), 
            asyncio.create_task(self.send_and_recieve_packets()),
        ]
        tasks.append(
            asyncio.create_task(self.monitor(tasks))
        )
        await asyncio.wait(tasks)
