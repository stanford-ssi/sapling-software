import asyncio
import os

import pytest

from sapling.utils.ftp import FileTransferProtocol
from sapling.utils.ptp import AsyncPacketTransferProtocol

from tests.runner import BaseRunner

class TestRunner(BaseRunner):

    def __init__(self, *args, **kwargs):
        super(TestRunner, self).__init__(*args, **kwargs)
        self.done = False
        self.ptp = AsyncPacketTransferProtocol(self.board.data_receive_stream, self.board.data_send_stream)
        self.ftp = FileTransferProtocol(self.ptp.outbox, self.ptp.inbox)

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

    async def recieve_packets(self):
        while not self.tasks_running:
            await asyncio.sleep(0.1)
        self.LOGGER.info("PTP receving packets from PyCubed")
        while True:
            await self.ptp.receive()

    async def send_packets(self):
        while not self.tasks_running:
            await asyncio.sleep(0.1)
        self.LOGGER.info("PTP sending packets to PyCubed")
        while True:
            await self.ptp.send()

    async def receive_file(self):
        test_file = 'hello.txt'
        
        # setup
        while not self.tasks_running:
            await asyncio.sleep(0.1)
        
        # request file
        self.LOGGER.info(f"Sending request to PyCubed for {test_file}")
        await self.ftp.request_file(test_file)
        
        # print file TODO replace with assert
        with open(test_file) as f:
            for line in f.readlines():
                print(line)
        
        # cleanup
        self.LOGGER.info("deleting hello.txt")
        os.remove("hello.txt")


    async def run(self):
        """Runs a test. Logs output before the entry point of main.py on debug,
        and output after on info. Fails current pytest if `ERROR` is present 
        in output, and passes (does not call pytest.xfail) if `TEST PASSED` is
        present.
        """
        self.test_started = False
        self.tasks_running = False
        await asyncio.wait([
            asyncio.create_task(self.repl()),
            asyncio.create_task(self.recieve_packets()),
            asyncio.create_task(self.send_packets()),
            asyncio.create_task(self.receive_file())
        ])
