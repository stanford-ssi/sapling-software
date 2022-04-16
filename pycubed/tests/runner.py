import pytest

class BaseRunner:

    def __init__(self, board, LOGGER):
        self.board = board
        self.LOGGER = LOGGER

    def run(self):
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
                    