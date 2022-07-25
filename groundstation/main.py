from pycubed import cubesat

cubesat.radio1.ack_retries = 2
cubesat.radio1.ack_wait = 2
cubesat.radio1.node = 0xAB # this radio's radiohead ID
cubesat.radio1.destination = 0xFA # target sat's radiohead ID

# create a command dictionary to make this easier
commands = {
    # command name : command code
    'no-op':b'\x8eb',                   # does nothing
    'hreset':b'\xd4\x9f',               # hard reset
    ######## cmds with args ########
    'shutdown':b'\x12\x06',             # shutdown sat
    'query':b'8\x93',                   # eval
    'exec_cmd':b'\x96\xa2',             # exec
    'send_file': b'\x48\x6f',           # send file
}

# initialize cmd variable with default pass-code
cmd =  b'p\xba\xb8C'

# next specify cmd by editing the string below
CHOOSE_CMD = 'send_file'
print('\nWill send command after hearing beacon:',CHOOSE_CMD)

# then we add the cmd code for our chosen cmd string
cmd += commands[CHOOSE_CMD]

FILENAME = 'tree.jpg'

# finally we add any arguments (if necessary)
# P.S. we're doing it this way to illustrate each piece that goes into the cmd packet
if CHOOSE_CMD == 'shutdown':
    cmd += b'\x0b\xfdI\xec' # shutdown confirmation code
elif CHOOSE_CMD == 'query':
    cmd += b'cubesat.f_deployed' # our query argument. try your own!
elif CHOOSE_CMD == 'exec_cmd':
    cmd += b'a=1\nprint(a)'
elif CHOOSE_CMD == 'send_file':
    cmd += FILENAME


while True:
    response=cubesat.radio1.receive(timeout=10)
    if response is not None:
        print('Beacon Packet:',response)
        ack = cubesat.radio1.send_with_ack(cmd)
        if ack is not None:
            if ack: print('ACK RSSI:',cubesat.radio1.last_rssi-137)
        # only listen for a response if we're expecting one
        if CHOOSE_CMD in ('shutdown','query','exec_cmd'):
            response=cubesat.radio1.receive(timeout=10)
            if response is not None:
                print('Response:',response)
        if CHOOSE_CMD == 'send_file':
            num_packets = cubesat.r_aptp._receive_packet_sync()
            missing = cubesat.r_ftp.receive_file_sync(f'{FILENAME}', num_packets, from_sd=True)
            print(f"missing packets: {missing}")
            print("Received file!")