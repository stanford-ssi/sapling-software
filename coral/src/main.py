import os
import multiprocessing as mp

# 3rd party library
import serial

# internal library
import ftp

def poweroff():
    os.system("sudo poweroff")

def ping(transport):
    transport.write(b'coral says hello!')

def take_picture(transport):
    transport.write(b'taking picture')

def send_file(transport):
    transport.write(b'sending file')

callbacks = {
    'poweroff': poweroff,
    'ping': ping,
    'take_picture': take_picture,
    'send_file': send_file,
}

class CoralProtocol(ftp.FileTransferProtocol):

    def __init__(self, transfer_protocol, data_queue):
        super().__init__(transfer_protocol)
        self.data_queue = data_queue

    # get packet actually reads
    def receive_packet_from_protocol(self):
        return super().readline()

    # override readline to read from the data queue
    def receive_packet(self):
        return data_queue.get()
        


def command_handler(task_queue, data_queue):
    while True:
        packet = f.receive_packet_from_protocol()

        # put task in back of task queue
        if 'command' in packet:
            command = packet['command']
            task_queue.put(callbacks[command])
        
        # forward data to worker
        else:
            data_queue.put(packet)


def worker(task_queue, data_queue):
    while True:
        # if there is a task
        if not task_queue.empty():
            # run the task
            task_queue.get()()


if __name__ == "__main__":
    task_queue = mp.Queue()
    data_queue = mp.Queue()
    serial_port = serial.Serial('/dev/ttyS1', baudrate=115200)
    comm_protocol = CoralProtocol(serial_port)

    worker_process = mp.Process(target=worker, args=(comm_protocol,task_queue,data_queue,))
    command_handler_process = mp.Process(target=command_handler, args=(comm_protocol,task_queue,data_queue,))

    # start the command handler and the worker
    worker_process.start()
    command_handler_process.start()
    worker_process.join()
    command_handler_process.join()

