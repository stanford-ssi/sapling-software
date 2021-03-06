import os, binascii
import math
import json

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
            
        return packet

class FileTransferProtocol:
    """A simple transfer protocol
    """

    def __init__(self, transfer_protocol):
        self._transfer_protocol = transfer_protocol
        self.ack = b'ACKACK'
        self.retransmit = b'RETRANSMIT'

    def send_packet(self, payload, ack=True, attempts=3):
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
        self._transfer_protocol.write(bin_packet)
        self._transfer_protocol.write(b'\n')
        for i in range(attempts):
            response = self._wait_for_ack()
            if response == 'RETRANSMIT':
                self._transfer_protocol.write(packet)
            elif response == 'ACKACK':
                return True
        return False

    def _wait_for_ack(self, timeout=20):
        """Wait for an ACK packet

        Args:
            timeout (int, optional): currently unused. Defaults to 20.

        Returns:
            (): CRC32 validated packet
        """
        packet = self._transfer_protocol.readline()
        try:
            packet = json.loads(packet)
        except ValueError:
            print("Failed to decode JSON")
        if self.crc32_packet(packet) != packet['c']:
            print(f"CRC32 failure on ACK: {packet}")
        return packet['d']
         
    def receive_packet(self):
        """receive a packet

        Returns:
            (): CRC32 validated packet
        """
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

    def send_file(self, filename, chunk_size=64):
        """Send a file

        Args:
            filename (str): path to file that will be sent
            chunk_size (int, optional): chunk sizes that will be sent. Defaults to 64.
        """
        with open(filename, 'rb') as f:
            stats = os.stat(filename)
            filesize = stats[6]
            
            # send the number of packets for the reader to expect
            self.send_packet(math.ceil(filesize / chunk_size))

            # send all the chunks
            for chunk, packet_num in self._read_chunks(f, chunk_size):
                chunk = binascii.b2a_base64(chunk)
                if not self.send_packet([packet_num, chunk.decode('ascii')]):
                    print(f"failed to send packet {packet_num}")

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
            print(f"type: {type(packet['d'])}\ndata: {packet['d']}\m")
        return binascii.crc32(packet_bytes, 0)

    def receive_file(self, filename, packet_length=64):
        """Receive a file

        Args:
            filename (str): path where file will be written
            packet_length (int, optional): currently unused. Defaults to 64.
        """
        with open(filename, 'ab+') as f:
            # get the number of expected packets
            init_packet = self.receive_packet()
            num_packets = int(init_packet)
            print(f"expecting to receive {num_packets} packets")

            # read all the packets and construct file
            for packet_num in range(num_packets):
                chunk = self.receive_packet()
                recvd_num, chunk = list(chunk)
                assert(packet_num == int(recvd_num))
                chunk = binascii.a2b_base64(chunk)
                f.write(chunk)
                os.sync()
                
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
                return
            counter += 1
