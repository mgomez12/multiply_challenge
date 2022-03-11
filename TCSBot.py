from telnetlib import Telnet
from robot import Robot

class TCSBot(Robot):
    def __init__(self, ip=None):
        Robot.__init__(self)
        print("initing")
        if ip:
            self.tn=Telnet(ip)
        else:
            self.tn = Telnet('192.168.0.1')
        self.attach()
        
    def send_cmd(self, s):
        tn.write(s.encode('ascii') + b"\n")
    def attach():
        self.send_cmd("attach 1")
    def release():
        self.send_cmd("attach 0")
    def shutdown():
        self.release()
        send_cmd("exit")
        

