import pytest 
from tests.runner import BaseRunner
import sapling.utils.ftp as ftp

class TestRunner(BaseRunner):

    def __init__(self, *args, **kwargs):
        super(TestRunner, self).__init__(*args, **kwargs)
        self.done = False
        self.ptp = ftp.PacketTransferProtocol(self.board.data_conn)

    async def repl(self):
        print(self.board)
        line = self.board.readline()
        if '----------------------------------------' in line:
            self.test_started = True
        if self.test_started:
            if "Running..." in line:
                self.tasks_running = True
            self.LOGGER.info(line)
            if "TEST PASSED" in line:
                self.LOGGER.info(line)
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
                    
    async def data(self):
        while True:
            if self.need_to_send_packet and self.tasks_running:
                #if time.time() > delay_time:
                self.LOGGER.info("Sending packet to PyCubed")
                ack = self.ptp.send_packet("hello from host")
                assert(ack)
                packet = self.ptp.receive_packet()
                self.LOGGER.info(packet)
                self.need_to_send_packet = False

    async def run(self):
        """Runs a test. Logs output before the entry point of main.py on debug,
        and output after on info. Fails current pytest if `ERROR` is present 
        in output, and passes (does not call pytest.xfail) if `TEST PASSED` is
        present.
        """
        self.test_started = False
        self.need_to_send_packet = True
        self.tasks_running = False    
        
                    
