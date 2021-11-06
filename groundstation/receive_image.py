from pycubed import cubesat

def receive_image(filename):
    packet_count = 0
    with open(f"/sd/{filename}", "ab+") as image:
        print(f"listening for image {filename}:")
        while True:
            packet = cubesat.radio1.receive(timeout=10, keep_listening=True, with_ack=True)
            if not packet:
                continue
            packet = bytearray(packet)
            image.write(packet)
            packet_count += 1
            if packet_count % 10 == 0:
                (f"packets recieved: {packet_count}")
            if len(packet) < 251:
                break
        print(f"packets recieved: {packet_count}")