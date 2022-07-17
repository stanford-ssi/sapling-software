import asyncio
import binascii
import json
import logging

LOGGER = logging.getLogger(__name__)


class AsyncPacketTransferProtocol:
    """A simple transfer protocol
    """

    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer
        self.ack = 'ACKACK'
        self.retransmit = 'RETRANSMIT'
        self.inbox = asyncio.Queue()
        self.outbox = asyncio.Queue()

    # user coroutines
    async def send(self):
        while True:
            packet = await self.outbox.pop()
            ack = self._send_packet(packet)
            #assert(ack)

    async def receive(self):
        while True:
            data = await self._receive_packet()

    # helper methods  
    async def _send_packet(self, payload, ack=True, attempts=3, timeout=10):
        """Send a packet

        Args:
            payload (str, int, list): data to be sent
            ack (bool): wait for received to acknowledge receipt of packet. Defaults to True.
            attempts (int, optional): number of attempts to make. Defaults to 3.

        Returns:
            _type_: _description_
        """
        bin_packet = self._send_packet_sync(payload)
        
        # await a response for a specified number of attempts
        for i in range(attempts):
            response = await self._wait_for_ack(timeout)
            if response == 'RETRANSMIT':
                self._transfer_protocol.write(bin_packet)
            elif response == 'ACKACK':
                return True
        return False

    async def _wait_for_ack(self, timeout):
        """Wait for an ACK packet

        Args:
            timeout (int, optional): currently unused. Defaults to 20.

        Returns:
            (): CRC32 validated packet
        """
        packet = await self.reader.readline()
        try:
            packet = json.loads(packet)
        except ValueError:
            print(f"Failed to decode JSON {packet}")
        if self.crc32_packet(packet) != packet['c']:
            print(f"CRC32 failure on ACK: {packet}")
        return packet['d']

    async def _receive_packet(self):
        #packet = await self.reader.readuntil(b'\n')
        packet = await self.reader.readline()
        try:
            packet = json.loads(packet)
        except ValueError: # json.decoder.JSONDecodeError:
            packet = json.loads(packet.decode('ascii'))
            print("Failed to decode JSON")
        if packet['c'] != self.crc32_packet(packet):
            await self._request_retransmit()
            print(f"CRC32 failure on, requesting retransmit: {packet}")
        self._send_ack()
        await self.inbox.put(packet['d'])
        return packet['d']

    def _send_ack(self):
        """Send an ACK packet
        """
        self._send_packet_sync(self.ack)

    def _request_retransmit(self):
        """Send an RTR packet
        """
        self._send_packet_sync(self.retransmit)

    def _send_packet_sync(self, data):
        bin_packet = self._create_packet(data)      
        self.writer.write(bin_packet)
        self.writer.write(b'\n')
        return bin_packet

    def _create_packet(self, data):
        packet = {}
        packet['d'] = data
        packet['c'] = self.crc32_packet(packet)
        bin_packet = json.dumps(packet).encode('ascii')
        return bin_packet

    # async def _request_retransmit(self):
    #     """Send a retransmit request
    #     """
    #     await self.send_packet(self.retransmit)

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

