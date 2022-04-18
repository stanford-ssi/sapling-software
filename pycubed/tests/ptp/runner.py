import pytest 
from tests.runner import BaseRunner
import sapling.utils.ftp as ftp
import asyncio

class TestRunner(BaseRunner):

    def __init__(self, *args, **kwargs):
        super(TestRunner, self).__init__(*args, **kwargs)
        self.done = False

    async def repl(self):
        print(self.board)
        line = self.board.readline()
        if '----------------------------------------' in line:
            test_started = True
        if test_started:
            if "Running..." in line:
                tasks_running = True
                # delay_time = time.time() + 0.0
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
            if need_to_send_packet and tasks_running:
                #if time.time() > delay_time:
                self.LOGGER.info("Sending packet to PyCubed")
                ack = f.send_packet("hello from host")
                assert(ack)
                packet = f.receive_packet()
                self.LOGGER.info(packet)
                need_to_send_packet = False

    async def run(self):
        """Runs a test. Logs output before the entry point of main.py on debug,
        and output after on info. Fails current pytest if `ERROR` is present 
        in output, and passes (does not call pytest.xfail) if `TEST PASSED` is
        present.
        """
        test_started = False
        f = ftp.PacketTransferProtocol(self.board.data_conn)
        need_to_send_packet = True
        tasks_running = False
        delay_time = 0;
        
                    
            
            
                    
