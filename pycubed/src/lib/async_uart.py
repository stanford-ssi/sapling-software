import busio

class AsyncUART(busio.UART):

    def __init__(self, *args, **kwargs):
        super(AsyncUART, self).init(args, kwargs)

    async def readline(self):
        """Yields if there are no characters waiting.
        TODO: reimplement so that it yields if there is a gap in
        characters recieved while reading a line.

        Returns:
            (): line of data
        """
        if not self.uart.in_waiting:
            yield
        else:
            yield super().readline()