# PyCubed <> Coral

## PyCubed Side

Coral interface class (like the Satellite class)
Member variable inside of Satellite object

What must it do?

- Send commands
- Send/recieve files
- Put into sleep mode for some amount of time

## Coral Side

- Python loop that asynchronously waits for commands from UART and dispatches them
- Linux Service that keeps the python script running after reboot. Reference: <https://www.digitalocean.com/community/tutorials/how-to-configure-a-linux-service-to-start-automatically-after-a-crash-or-reboot-part-1-practical-examples>

## Transfer Protocol

- UART: Coral <> PyCubed (potentially plagued by resets on either side)
- LoRA: PyCubed <> PyCubed via Radio (very small packets)
- USB: PyCubed (SD Card) <> Computer (normal)

### Steps to transmit a file

1. encode file as base 64

```CircuitPython
# encode
binascii.b2a_base64
# decode
binascii.a2b_base64
```

2. Break file into chunks
   Calculate CRC32 (need to recompile into the binascii module)
   Create packet
   Send packet via serial

basic packet structure

```json
{
    "metadata": [
        "packet_number",
        "origin_id",
        "crc32",
    ],
    "payload": "base64_data_chunk" 
}

```

(blank line at the end)

*base64 is verbose, so perhaps CBOR or some other alternative is better*
However, for now we should use this because its built-inish to circuitpython.
Perhaps `flynn` or `flunn` would work: <https://github.com/fritz0705/flynn>
(`cbor2` would work on coral)

—

Steps to receive a file:

1. send a request for some file
2. receive notification that file is ready
3. loop: read until blank line while writing to the SD Card
4. re-request missed packets (X number of times)
