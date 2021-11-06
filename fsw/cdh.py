import time

commands = {
    b'\x8eb': 'no-op',
    b'\xd4\x9f': 'hreset',
    b'\x12\x06': 'shutdown',
    b'\x44\x49': 'downlink_image',
    b'\x44\x54': 'detailed_telemetry',
    b'\x43\x43': 'coral_command',
    b'8\x93': 'query',
    b'\x96\xa2': 'exec_cmd',
}

########### commands without arguments ###########
def noop(self):
    self.debug('no-op')
    pass

def hreset(self):
    self.debug('Resetting')
    try:
        self.cubesat.radio1.send(data=b'resetting')
        self.cubesat.micro.on_next_reset(cubesat.micro.RunMode.NORMAL)
        self.cubesat.micro.reset()
    except:
        pass

########### commands with arguments ###########

def shutdown(self,args):
    # make shutdown require yet another pass-code
    if args == b'\x0b\xfdI\xec':
        self.debug('valid shutdown command received')
        # set shutdown NVM bit flag
        self.cubesat.f_shtdwn=True
        # stop all tasks
        for t in self.cubesat.scheduled_tasks:
            self.cubesat.scheduled_tasks[t].stop()
        self.cubesat.powermode('minimum')

        """
        Exercise for the user:
            Implement a means of waking up from shutdown
            See beep-sat guide for more details
            https://pycubed.org/resources
        """
        while True:
            time.sleep(100000)

def downlink_image(self,args):
    # add error handling here
    self.debug('downlinking image: {}'.format(args))
    with open(args, "rb") as image:
        packet_count = 0
        timer = time.time()
        while True:
            chunk = image.read(251)
            if chunk == b'':
                break
            self.radio1.send_with_ack(chunk)
            packet_count += 1
            if packet_count % 10 == 0:
                self.debug(f"packets sent: {packet_count}")    
        self.debug(f"total packets sent: {packet_count} in {time.time() - timer} seconds")

def detailed_telemetry(self,args):
    # send down detailed telemetry from the cubesat
    pass

def coral_command(self,args):
    # send content of the arguments to the google coral
    pass

def query(self,args):
    self.debug('query: {}'.format(args))
    self.cubesat.radio1.send(data=str(eval(args)))

def exec_cmd(self,args):
    self.debug('exec: {}'.format(args))
    exec(args)
