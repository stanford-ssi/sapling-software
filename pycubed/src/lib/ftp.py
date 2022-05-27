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
import json
from file_utils import FileLockGuard

class SimpleQueue(list):

    def __init__(self, *args, **kwargs):
        super(SimpleQueue, self).__init__(*args, **kwargs)

    def pushleft(self, item):
        super().insert(0, item)

    async def pop(self):
        if len(self):
            return super().pop()
        else:
            yield

    def empty(self):
        return len(self) == 0

class RadioProtocol:

    def __init__(self, cubesat):
        self.cubesat = cubesat

    def write(self, packet):
        num_packets = math.ceil(len(packet)/250)
        for i in range(num_packets):
            self.cubesat.radio1.send(packet[i*250:(i+1)*250])

    def readline(self):
        packet = b''
        while True:
            try:
                radio_packet = bytes(self.cubesat.radio1.receive(keep_listening=True))
                print(f"received radio packet: {radio_packet} ({type(radio_packet)})")
                if '\n' in radio_packet:
                    break
                packet += radio_packet # check this
            except TypeError:
                print(f"received empty radio packet")

class PacketTransferProtocol:
    """A simple transfer protocol
    """

    def __init__(self, transfer_protocol):
        self._transfer_protocol = transfer_protocol
        self.ack = 'ACKACK'
        self.retransmit = 'RETRANSMIT'
        self.inbox = SimpleQueue()
        self.outbox = SimpleQueue()

    async def send(self):
        print(f"outbox: {self.outbox}")
        if self.outbox.empty():
            return False
        while not self.outbox.empty():
            packet = await self.outbox.pop()
            ack = await self.send_packet(packet)
            assert(ack)
            print("sent a packet!")
        return True
            
    async def send_packet(self, payload, ack=True, attempts=3):
        """Send a packet

        Args:
            payload (str, int, list): data to be sent
            ack (bool): wait for received to acknowledge receipt of packet. Defaults to True.
            attempts (int, optional): number of attempts to make. Defaults to 3.

        Returns:
            _type_: _description_
        """
        packet = {}
        packet['d'] = payload
        packet['c'] = self.crc32_packet(packet)
        bin_packet = json.dumps(packet).encode('ascii')
        assert(isinstance(bin_packet, bytes))
        self._transfer_protocol.write(bin_packet)
        self._transfer_protocol.write(b'\n')
        for i in range(attempts):
            response = await self._wait_for_ack()
            if response == 'RETRANSMIT':
                self._transfer_protocol.write(packet)
            elif response == 'ACKACK':
                return True
        return False

    async def _wait_for_ack(self, timeout=10):
        """Wait for an ACK packet

        Args:
            timeout (int, optional): currently unused. Defaults to 20.

        Returns:
            (): CRC32 validated packet
        """
        packet = await self._transfer_protocol.readline()
        try:
            packet = json.loads(packet)
        except ValueError:
            print("Failed to decode JSON")
        if self.crc32_packet(packet) != packet['c']:
            print(f"CRC32 failure on ACK: {packet}")
        return packet['d']

    def receive_packet_sync(self):
        packet = self._transfer_protocol.readline()
        try:
            packet = json.loads(packet)
        except ValueError: # json.decoder.JSONDecodeError:
            packet = json.loads(packet.decode('ascii'))
            print("Failed to decode JSON")
        if packet['c'] != self.crc32_packet(packet):
            self._request_retransmit()
            print(f"CRC32 failure on : {packet}")
        self._send_ack()
        self.inbox.pushleft(packet['d'])
        return packet['d']
         
    async def receive_packet(self):
        """receive a packet

        Returns:
            (): CRC32 validated packet
        """
        packet = await self._transfer_protocol.readline()
        try:
            packet = json.loads(packet)
        except ValueError: # json.decoder.JSONDecodeError:
            packet = json.loads(packet.decode('ascii'))
            print("Failed to decode JSON")
        if packet['c'] != self.crc32_packet(packet):
            self._request_retransmit()
            print(f"CRC32 failure on : {packet}")
        self._send_ack()
        self.inbox.pushleft(packet['d'])
        return packet['d']

    def _send_ack(self):
        """Send an ACK packet
        """
        packet = {}
        packet['d'] = self.ack
        packet['c'] = self.crc32_packet(packet)
        bin_packet = json.dumps(packet).encode('ascii')
        self._transfer_protocol.write(bin_packet)
        self._transfer_protocol.write(b'\n')

    def _request_retransmit(self):
        """Send a retransmit request
        """
        self.send_packet(self.retransmit)

    def crc32_packet(self, packet):
        """Calculate Cyclic Redundancy Check (CRC) of a piece of data using the
        CRC-32 algorithm

        Args:
            packet (str, bytes, list, int): a piece of data

        Returns:
            int: CRC-32 value
        """
        if isinstance(packet['d'], str):
            packet_bytes = packet['d'].encode('ascii')
        elif isinstance(packet['d'], bytes):
            packet_bytes = packet['d']
        elif isinstance(packet['d'], list):
            packet_bytes = str(packet['d']).encode('ascii')
        elif isinstance(packet['d'], int):
            packet_bytes = bytes(packet['d'])
        else:
            print("\n\npacket did not contain either binary or string data...\n\n")
            print(f"type: {type(packet['d'])}\ndata: {packet['d']}\n")
        return binascii.crc32(packet_bytes, 0)


class FileTransferProtocol:

    def __init__(self, inbox, outbox):
        self.inbox = inbox
        self.outbox = outbox

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
                chunk = self.inbox.pop()
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
            self.outbox.pushleft(math.ceil(filesize / chunk_size))

            # send all the chunks
            for chunk, packet_num in self._read_chunks(f, chunk_size):
                print(chunk)
                chunk = binascii.b2a_base64(chunk)
                self.outbox.pushleft([packet_num, chunk.decode('ascii')])
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
