import json
import socket
from channel_constants import *
import time

class Network:
    def __init__(self,number):
        self.number= number
        self.data = []
        self.start_channel()

    def start_channel(self):
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
                    self.data.append(recv)
        print(recv)
        try:
            '''if self.data includes json file'''
            self.data=''.join(self.data)
            self.data=json.loads(self.data)
            '''self.host and self.port include ip and port for channel server side '''
            self.host=self.data['ip']
            self.port=self.data['port']
            self.programs=self.data['programs']
            print(f'host:{self.host}\nport:{self.port}\nprograms:{self.programs}')
        except:
            '''if self.data does not include json file'''
            pass
    
    def receive_liveProgram(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
            soc.connect((host, port))
        pass


if __name__=='__main__':
    network=Network(3)