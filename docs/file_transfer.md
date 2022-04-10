# PyCubed <> Coral

## PyCubed Side

## Transfer Protocol

1. encode file as base 64

```CircuitPython
# encode
binascii.b2a_base64
# decode
binascii.a2b_base64
```

2. Break file into chunks
   (Calculate CRC32)
   Create packet
   Send packet via serial

opening packet

```json
{
    "s": "num_packets_in_file",
    "c": "crc32_of_num_packets_in_file"
}
```

file packet structure

```json
{
    "n": "packet_number",
    "payload": "base64_data_chunk",
    "crc32": "crc32 of packet - crc32" // we want to include the packet number 
                                       // in the CRC
}

```

|PyCubed|Coral|
|-------|-----|
| Send request for file | |
| Wait for response |
| | Send opening packet with metadata |
| | Wait for ACK |
| Check CRC32 matches the metadata packet | |
| Request retransmit or send ACK | |

*base64 is verbose, so perhaps CBOR or some other alternative is better*
