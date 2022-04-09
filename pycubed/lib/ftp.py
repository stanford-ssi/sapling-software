import os, binascii
import math
import json

class FakeTransferProtocol:

    def __init__(self):
        pass

    def write(self, packet):
        print(f"sending packet:\n{packet}\n")

    def receive(self):
        return {
            'd': "fake data",
        }

    def readline(self):
        return {
            'd': "ACKACK",
            'c': 1837295334
        }

class FileTransferProtocol:

    def __init__(self, transfer_protocol):
        self._transfer_protocol = transfer_protocol
        self.ack_packet = {}
        self.ack_packet['d'] = 'ACKACK'
        self.ack_packet['c'] = self.crc32_packet(self.ack_packet)
        self.ack_packet = bytes(json.dumps(self.ack_packet), 'ascii')
        self.retransmit_packet = {}
        self.retransmit_packet['d'] = 'RETRANSMIT'
        self.retransmit_packet['c'] = self.crc32_packet(self.retransmit_packet)
        self.retransmit_packet = bytes(json.dumps(self.retransmit_packet), 'ascii')

    def send_packet(self, payload, attempts=3):
        packet = {}
        packet['d'] = payload
        packet['c'] = self.crc32_packet(packet)
        bin_packet = bytes(json.dumps(packet), 'ascii')
        self._transfer_protocol.write(bin_packet)
        self._transfer_protocol.write(b'\n')
        for i in range(attempts):
            response = self._wait_for_ack()
            print(f"recieved response: {response}")
            if response == 'RETRANSMIT':
                self._transfer_protocol.write(packet)
            elif response == 'ACKACK':
                return True
        return False

    def _wait_for_ack(self, timeout=20):
        packet = self._transfer_protocol.readline()
        try:
            packet = json.loads(packet)
        except ValueError:
            print("Failed to decode JSON")
        if self.crc32_packet(packet) != packet['c']:
            print(f"CRC32 failure on ACK: {packet}")
        return packet['d']
         
    def recieve_packet(self):
        packet = self._transfer_protocol.readline()
        try:
            packet = json.loads(packet)
        except ValueError: # json.decoder.JSONDecodeError:
            print("Failed to decode JSON")
        if packet['c'] != self.crc32_packet(packet):
            self._request_retransmit()
        print(f"CRC32 failure on : {packet}")
        self._send_ack()
        return packet['d']

    def _send_ack(self):
        self._transfer_protocol.write(self.ack_packet)

    def _request_retransmit(self):
        self._transfer_protocol.write(self.retransmit_packet)

    def send_file(self, filename, packet_length=1024):
        with open(filename, 'rb') as f:
            stats = os.stat('/sd' + filename)
            filesize = stats[6]
            
            # send the number of packets for the reader to expect
            self.send_packet([math.ceil(filesize / packet_length)])

            # send all the chunks
            for chunk, packet_num in self._read_chunks(f):
                self.send_packet([packet_num, binascii.b2a_base64(chunk)])

    def crc32_packet(self, packet):
        packet_bytes = bytes(packet['d'], 'ascii')
        return binascii.crc32(packet_bytes, 0)

    def recieve_file(self, filename, packet_length=1024):
        with open(filename, 'wb+') as f:
            # get the number of expected packets
            init_packet = self.recieve_packet()
            num_packets = init_packet

            # read all the packets and construct file
            for packet_num in range(num_packets):
                pass
                
    def _read_chunks(self, infile, chunk_size=1024):
        counter = 0
        while True:
            chunk = infile.read(chunk_size)
            if chunk:
                yield (chunk, counter)
            else:
                return
            counter += 1
            