from ..runner import BaseRunner
import pytest 
import adafruit_board_toolkit.circuitpython_serial

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
        while True:
            print(self.board)
            line = self.board.readline()
            if '----------------------------------------' in line:
                test_started = True
            if test_started:
                self.LOGGER.info(line)
            else:
                self.LOGGER.debug(line)
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
                    
