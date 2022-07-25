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
import gc

from file_utils import FileLockGuard

class FileTransferProtocol:

    def __init__(self, ptp):
        self.inbox = ptp.inbox
        self.outbox = ptp.outbox
        self.ptp = ptp

    async def request_file(self, remote_path, local_patb):
        """Receive a file

        Args:
            filename (str): path where file will be written
        """
        # request file
        request = f"GET\n{remote_path}"
        await self.outbox.put(request)
        # first packet is the number of packets in the file
        while True:
            num_packets = await self.inbox.get()
            if not num_packets:
                yield
                continue
            else:
                break
        try:
            num_packets = int(num_packets)
        except ValueError as e:
            print(e)
        with open(local_patb, 'ab+') as f:
            # read all the packets and construct file
            for packet_num in range(num_packets):
                chunk = await self.inbox.get()
                recvd_num, chunk = list(chunk)
                assert(packet_num == int(recvd_num))
                chunk = binascii.a2b_base64(chunk) #TODO
                f.write(chunk)
                os.sync()

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

    def receive_file_sync(self, filename, num_packets, from_sd=False):
        """Receive a file

        Args:
            filename (str): path where file will be written
        """
        new_filename = ''
        if from_sd == True:
            new_filename = f"/sd/{filename}"
        else:
            new_filename = filename
        print(new_filename)
        with open(new_filename, 'ab+') as f:
            # get the number of expected packets
            print(f"expecting to receive {num_packets} packets")
            missing = {i for i in range(num_packets)}
            # read all the packets and construct file
            for packet_num in range(num_packets):
                chunk = self.ptp._receive_packet_sync()
                recvd_num, chunk = list(chunk)
                missing.remove(int(recvd_num))
                chunk = binascii.a2b_base64(chunk) #TODO
                f.write(chunk)
                os.sync()
        return missing

    async def send_file(self, filename, chunk_size=64):
        """Send a file

        Args:
            filename (str): path to file that will be sent
            chunk_size (int, optional): chunk sizes that will be sent. Defaults to 64.
        """
        
        #async with FileLockGuard(filename, 'rb') as f:
        with open(filename, 'rb') as f:
            print(filename)
            stats = os.stat(filename)
            filesize = stats[6]
            
            # send the number of packets for the reader to expect
            while True:
                success = await self.outbox.put(math.ceil(filesize / chunk_size))
                print("put the filesize")
                if not success:
                    yield
                else:
                    break
            
            # send all the chunks
            for chunk, packet_num in self._read_chunks(f, chunk_size):
                chunk = binascii.b2a_base64(chunk)
                
                while True:
                    await self.outbox.put([packet_num, chunk.decode('ascii')])
                    if not success:
                        yield
                    else:
                        break
                # TODO add async hand over if the queue is full
    
    def send_file_sync(self, filename, chunk_size=64):
        # filename='/sd/1kb.png'
        # chunk_size=64
        with open(filename, 'rb') as f:
            print(filename)
            stats = os.stat(filename)
            filesize = stats[6]
            
            # send the number of packets for the reader to expect
            self.ptp._send_packet_sync(math.ceil(filesize / chunk_size), ack=False)
            
            # send all the chunks
            for chunk, packet_num in self._read_chunks(f, chunk_size):
                chunk = binascii.b2a_base64(chunk)
                
                self.ptp._send_packet_sync([packet_num, chunk.decode('ascii')], ack=False)
                    
                
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
