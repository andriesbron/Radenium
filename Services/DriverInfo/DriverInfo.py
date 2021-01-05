
from Core.Service import BaseService
import time

try:
    import serial.tools.list_ports as port_list
except:
    print("You should run in a terminal: pip3 install serial and pip3 install pyserial")

#todo rename this class
class DriverInfo(BaseService):
    def __init__(self, events):
        super().__init__(events)
        self.setTitle("Driver Info service for applications")
        self.ports=[]
        self.portlist={}
        
    def scanPorts(self):
        self.ports=list(port_list.comports ())
        i=0
        for port, desc, hwid in sorted (self.ports):
            self.portlist[str(i)] = str(port)
            i+=1

        return self.portlist

    def getPortList(self):
        return self.portlist


