import asyncio
import pathlib

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
        self.LOGGER.info("This test does not return and can be escaped manually with ctrl-c")
        while True:
            line = await self.board.readline()
            if '----------------------------------------' in line:
                self.test_started = True
            if self.test_started:
                self.LOGGER.info(line)
                if "Running..." in line:
                    self.tasks_running = True
                if "TEST PASSED" in line:
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
            asyncio.create_task(self.send_and_recieve_packets()),
        ]
        tasks.append(
            asyncio.create_task(self.monitor(tasks))
        )
        await asyncio.wait(tasks)
