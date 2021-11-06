#!/usr/bin python
# usage get_file.py <BOARD_NAME> <FILE_PATH>
import argparse
from pathlib import Path
import serial
import time
import shutil

def main(args):
    Path(f'./board_backups/{args.board}').mkdir(exist_ok=True)
    print(f"caching main.py from {args.board} to\n")
    shutil.copy2(f'/Volumes/{args.board}/main.py', f'./board_backups/{args.board}/main.py')

    # copy worker script to the target (and overwrite the old one)
    shutil.copy('./get_file_pycubed_side.py', f'/Volumes/{args.board}/main.py')
    time.sleep(1)

    # open connection to target
    uart = serial.Serial('/dev/tty.usbmodem1301', timeout = 5)
    command_string = f"send_me_the_fileXXX{args.filename}ZZZ"

    # print('resetting board')
    # uart.write(b'\x04') # ctrl-c
    # uart.write(b'\x0D') # return
    # uart.write(b'\x04') # ctrl-d

    time.sleep(1)
    with open(args.filename, 'ab+') as copied_file:
        file_found = False
        while True:
            print('asking for next packet...')
            print(f'command string: {command_string}')
            uart.write(bytes(command_string, 'ascii'))
            chunk = uart.read(4096)
            start_indice = 0
            end_indice = 4096
            if not file_found:
                # catch errors here
                if chunk.find(b"BEGINNING_OF_FILE"):
                    start_indice = chunk.find(b"BEGINNING_OF_FILE") + len(b"BEGINNING_OF_FILE")
                    file_found = True
                else:
                    continue
            # write the final chunk
            print(f'received chunk of length: {len(chunk)}')
            if len(chunk) <= 4096:
                print(f'weirdly small chunk of length, dumping:\n')
                print(chunk)
                end_indice = len(chunk)
                copied_file.write(chunk[start_indice:end_indice])
                break
            # write a full chunk
            copied_file.write(chunk[start_indice:end_indice])
        uart.close()
    
    print(f"restoring cached main.py to {args.board}")
    shutil.copy(f'./board_backups/{args.board}/main.py', f'/Volumes/{args.board}/main.py')

parser = argparse.ArgumentParser()
parser.add_argument("board")
parser.add_argument("filename")
args = parser.parse_args()

main(args)