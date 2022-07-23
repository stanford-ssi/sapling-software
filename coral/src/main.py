import asyncio

import serial_asyncio

import sapling.utils.ftp as ftp
import sapling.utils.ptp as ptp

from coral_camera import CoralCamera

class CoralManager:

    def __init__(self, url):
        self.url = url
        self.init_sem = asyncio.Semaphore(0)
        self.camera = CoralCamera()
        
    async def connect_to_pycubed(self, baudrate=9600):
        self.read_stream, self.write_stream = await serial_asyncio.open_serial_connection(url=str(self.url), baudrate=baudrate)
        self.ptp = ftp.AsyncPacketTransferProtocol(self.read_stream, self.write_stream)
        self.connected = True
        self.init_sem.release()

    async def command_handler(self):
        async with self.init_sem:
            while True:
                await self.ptp._receive_packet()

    async def write(self):
        self.debug("starting writer")
        await self.ptp.send()
    
    async def read(self):
        self.debug("starting reader")
        await self.ptp.receive()

    async def main(self):
        self.tasks_running = False
        await asyncio.wait([
            asyncio.create_task(self.connect_to_pycubed()),
            asyncio.create_task(self.command_handler()),
        ])

def main():
    loop = asyncio.get_event_loop()
    cm = CoralManager()
    try:
        loop.run_until_complete(cm.main())
    finally:
        loop.close()

if __name__ == "__main__":
    main()