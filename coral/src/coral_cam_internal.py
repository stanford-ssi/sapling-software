import asyncio
import subprocess

class CoralCamera:

    def __init__(self):
        self.name = 'camera'

    async def take_picture(self):
        proc = await asyncio.create_subprocess_exec(
            'snapshot',
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        print("hello")

        # wait for instructions linee
        line = await self.readline(proc)
        print("reads line")
        assert line == "Press space to take a snap, r to refocus, or q to quit"
        await asyncio.sleep(0.05)

        # send picture command
        proc.stdin.write(' ')
        await proc.stdin.drain()
        line = await self.readline(proc)
        assert "Saving image: " in line
        image_name = line.replace("Saving image:", "")

        # close the process
        proc.stdin.write('q')
        await asyncio.sleep(0.05)
        proc.stdin.close()
        return image_name

    async def readline(self, proc):
        data = await proc.stderr.readline()
        print(data)
        line = data.decode('ascii').rstrip()
        return line

    def take_picture_sync(self):
        proc = subprocess.Popen(
            'snapshot',
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        print("hello")

        # wait for instructions linee
            line = proc.stdout.readline()
        line = line.decode('ascii').rstrip()
        assert line == "Press space to take a snap, r to refocus, or q to quit"

        # send picture command
        proc.stdin.write(b' ')
        line = proc.stdout.readline()
        line = line.decode('ascii').rstrip()
        assert "Saving image: " in line
        image_name = line.replace("Saving image: ", "")
        print(image_name)

        # close the process
        proc.stdin.write(b'q')
        retval = proc.wait()
        return image_name

if __name__ == "__main__":
    cc = CoralCamera()
    cc.take_picture_sync()
    # loop = asyncio.get_event_loop()
    # try:
    #     loop.run_until_complete(cc.take_picture())
    # finally:
    #     loop.close()
    