"""
`ftp`
====================================================

Very simple CircuitPython compatible file transfer protocol

* Author(s): 
 - Flynn Dreilinger

Implementation Notes
--------------------

"""
import os, binascii
import math
from file_utils import FileLockGuard

class FileTransferProtocol:

    def __init__(self, ptp):
        self.inbox = ptp.inbox
        self.outbox = ptp.outbox

    async def receive_file(self, filename, num_packets):
        """Receive a file

        Args:
            filename (str): path where file will be written
        """
        async with FileLockGuard(filename, 'ab+') as f:
            # get the number of expected packets
            print(f"expecting to receive {num_packets} packets")

            # read all the packets and construct file
            for packet_num in range(num_packets):
                chunk = await self.inbox.get()
                recvd_num, chunk = list(chunk)
                assert(packet_num == int(recvd_num))
                chunk = binascii.a2b_base64(chunk) #TODO
                f.write(chunk)
                os.sync()

    async def send_file(self, filename, chunk_size=64):
        """Send a file

        Args:
            filename (str): path to file that will be sent
            chunk_size (int, optional): chunk sizes that will be sent. Defaults to 64.
        """
        async with FileLockGuard(filename, 'rb') as f:
            stats = os.stat(filename)
            filesize = stats[6]
            
            # send the number of packets for the reader to expect
            await self.outbox.put(math.ceil(filesize / chunk_size))

            # send all the chunks
            for chunk, packet_num in self._read_chunks(f, chunk_size):
                print(f"sending chunk: {chunk}")
                chunk = binascii.b2a_base64(chunk)
                await self.outbox.put([packet_num, chunk.decode('ascii')])
                # TODO add async hand over if the queue is full

                
    def _read_chunks(self, infile, chunk_size=64):
        """Generator that reads chunks of a file

        Args:
            infile (str): path to file that will be read
            chunk_size (int, optional): chunk sizes that will be returned. Defaults to 64.

        Yields:
            bytes: chunk of file
        """
        counter = 0
        while True:
            chunk = infile.read(chunk_size)
            if chunk:
                yield (chunk, counter)
            else:
                break
            counter += 1
