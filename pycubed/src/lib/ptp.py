import binascii
import json
import gc

from async_wrappers import AsyncQueue

class AsyncPacketTransferProtocol:
    """A simple transfer protocol
    """

    def __init__(self, protocol): # todo rewrite this with a reader and a writer
        self.protocol = protocol
        self.ack = 'ACKACK'
        self.retransmit = 'RETRANSMIT'
        self.inbox = AsyncQueue() # TODO move to async wrappers
        self.outbox = AsyncQueue()

    # user coroutines
    async def send(self):
        while True:
            packet = await self.outbox.get()
            if not packet:
                yield # never thought this day would come. TODO: switch to asyncio (from tasko)
                continue
            noack = await self._send_packet(packet, ack=False)
            #gc.collect()

    async def receive(self):
        while True:
            data = await self._receive_packet()
            #gc.collect()

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
        bin_packet = self._send_packet_sync(payload, ack)
        
        # await a response for a specified number of attempts
        if ack:
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
        packet = await self.protocol.readline()
        try:
            packet = json.loads(packet)
        except ValueError:
            print(f"Failed to decode JSON {packet}")
        if self.crc32_packet(packet) != packet['c']:
            print(f"CRC32 failure on ACK: {packet}")
        return packet['d']

    async def _receive_packet(self):
        packet = await self.protocol.readline()
        try:
            packet = json.loads(packet)
        except ValueError: # json.decoder.JSONDecodeError:
            packet = json.loads(packet.decode('ascii'))
            print("Failed to decode JSON")
        if packet['c'] != self.crc32_packet(packet):
            await self._request_retransmit()
            print(f"CRC32 failure on, requesting retransmit: {packet}")
        payload = packet['d']
        if 'a' in packet:
            self._send_ack()
        while True:
            success = await self.inbox.put(payload)
            if not success:
                yield
            else:
                break
        return payload

    def _send_ack(self):
        """Send an ACK packet
        """
        self._send_packet_sync(self.ack)

    def _request_retransmit(self):
        """Send an RTR packet
        """
        self._send_packet_sync(self.retransmit)

    def _send_packet_sync(self, data, ack=False):
        bin_packet = self._create_packet(data, ack)      
        self.protocol.write(bin_packet)
        self.protocol.write(b'\n')
        return bin_packet

    def _create_packet(self, data, ack=False):
        packet = {}
        packet['d'] = data
        packet['c'] = self.crc32_packet(packet)
        if ack:
            packet['a'] = 'a'
        bin_packet = json.dumps(packet).encode('ascii')
        return bin_packet

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