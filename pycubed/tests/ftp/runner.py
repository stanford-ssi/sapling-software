import pytest 
from tests.runner import BaseRunner
import sapling.utils.ftp as ftp
import asyncio
import os

class TestRunner(BaseRunner):

    def __init__(self, *args, **kwargs):
        super(TestRunner, self).__init__(*args, **kwargs)
        self.done = False
        self.ptp = ftp.AsyncPacketTransferProtocol(self.board.data_receive_stream, self.board.data_send_stream)

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
       
    async def send_and_packets(self):
        while not self.tasks_running:
            await asyncio.sleep(0.1)
        self.LOGGER.info("Sending packet to PyCubed")
        ack = await self.ptp.send_packet("send the file")
        assert(ack)

    async def send_and_receive_file(self):
        while not self.tasks_running:
            await asyncio.sleep(0.1)
        self.LOGGER.info("Sending packet to PyCubed")
        ack = await self.ptp.send_packet("send the file")
        assert(ack)
        self.LOGGER.info("Receiving file")
        num_packets = await self.ptp.receive_packet()
        self.LOGGER.info(f"Waiting for {num_packets} packets")
        self.ftp.receive_file("hello.txt", num_packets)
        self.LOGGER.info("Received hello.txt")
        with open("hello.txt") as f:
            print("\n")
            for line in f.readlines():
                print(line)
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
            asyncio.create_task(self.send_and_receive_packets()),
            asyncio.create_task(self.send_and_receive_file())
        ])
