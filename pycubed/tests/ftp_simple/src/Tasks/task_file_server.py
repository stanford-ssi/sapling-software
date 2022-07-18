from Tasks.template_task import Task
from protocol_shared import aptp, ftp

class task(Task):
    priority = 1
    frequency = 10 # once every 1s
    name = 'test task'
    color = 'red'

    schedule_later = True

    async def main_task(self):
        inbox = aptp.inbox
        outbox = aptp.outbox
        while True:
            packet = await inbox.get()
            #print(packet)
            if packet:
                break
            yield

        if "GET" in packet:
            self.debug("sending the file")
            await ftp.send_file("/sd/hello.txt")
        self.debug("TEST PASSED")
        yield