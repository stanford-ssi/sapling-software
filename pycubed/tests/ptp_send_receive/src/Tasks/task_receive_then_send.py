from Tasks.template_task import Task
from protocol_shared import aptp

class task(Task):
    priority = 1
    frequency = 10 # once every 1s
    name = 'test task'
    color = 'red'

    schedule_later = True

    async def main_task(self):
        inbox = aptp.inbox
        outbox = aptp.outbox
        self.debug("Receiving...")
        for i in range(100):
            packet = await inbox.get()
            if int(packet) != i:
                self.debug(f"Expecting packet {i}, received {packet}")
        self.debug(f"Received 100 sequenced packets from host")
        
        self.debug(f"Sending packets!")
        for i in range(100):
            await outbox.put(f"{i}")
        self.debug(f"Sent 100 packets!")
        self.debug(f"TEST PASSED")
        yield