import json
import socket
from chanel_constants import *
import time

class Network:
    def __init__(self,number):
        self.number= number
        self.programs = []
        self.get_ipPort()

    def get_ipPort(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
            soc.connect((host,port))
            msg=rqst_forTimeSchedule+f':{self.number}'
            soc.sendall(msg.encode(format))
            while True:
                recv=soc.recv(txt_messageSize).decode(format)
                if  recv==msg_receiving : 
                    recv=msg_receivingTimeSchedule
                    break
                elif recv==msg_active:
                    break
                else:
                    self.programs.append(recv)
        print(recv)
        self.programs=''.join(self.programs)
        self.programs=json.loads(self.programs)['Dune']



if __name__=='__main__':
    network=Network(1)