import json

class Coral:

    def __init__(self, uart):
        self.file_exchange = FileExchange(self.uart)

class PacketExchange:

    def __init__(self, uart):
        self.uart = uart

    async def send(self, raw):
        payload = json.dumps(raw) + "\n"
        b = bytearray()
        b.extend(payload)
        bytes_written = self.uart.write(b)
        return await self.receive()


    async def receive(self):
        # asynchronously wait for a packet
        # wait for the bytes available to be not empty
        # read the bytes in
        # decode the response packet, and send it over. 
            

class FileExchange:
    
    def __init__(self, uart):
        self.packet_exchange = PacketExchange(uart)
        pass

    async def request_file(self, filename):
        # send request for file
        payload = {
            'type': 'request_for_file',
            'args': {
                'filename': f'{filename}'
            }
        }
        await self.packet_exchange.send(payload)
        

    async def send_file(self, filename):
        # send request for file
        payload = {
            'type': 'sending_file',
            'args': {
                'filename': f'{filename}'
            }
        }
        await self.packet_exchange.send(payload)