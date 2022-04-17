import pytest 
from ..runner import BaseRunner
import ftp 

class TestRunner(BaseRunner):

    def __init__(self, *args, **kwargs):
        super(TestRunner, self).__init__(*args, **kwargs)

    def run(self):
        """Runs a test. Logs output before the entry point of main.py on debug,
        and output after on info. Fails current pytest if `ERROR` is present 
        in output, and passes (does not call pytest.xfail) if `TEST PASSED` is
        present.
        """
        test_started = False
        f = ftp.PacketTransferProtocol(self.board.data_conn)
        NEED_TO_SEND_PACKET = True
        while True:
            print(self.board)
            line = self.board.readline()
            if '----------------------------------------' in line:
                test_started = True
            if test_started:
                self.LOGGER.info(line)
                if "TEST PASSED" in line:
                    self.LOGGER.info(line)
                    break
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
                if NEED_TO_SEND_PACKET:
                    ack = f.send_packet("hello from host")
                    assert(ack)
                    packet = f.receive_packet_sync()
                    self.LOGGER.info(packet)
                    NEED_TO_SEND_PACKET = False
                    
            else:
                self.LOGGER.debug(line)
            
                    
