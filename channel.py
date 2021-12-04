import json
import socket
from channel_constants import *
import time
import struct
import threading
import warnings
warnings.filterwarnings("ignore")

class Network(threading.Thread):
    def __init__(self,number):
        threading.Thread.__init__(self)
        self.host = None
        self.port = None
        '''number of channel in network'''
        self.number= number
        '''temporary variable for receing data from main server'''
        self.data = []
        '''time-to-leave'''
        self.ttl=10
    
    def run(self):
        ret=self.start_channel()
        if ret:
            self.receive_liveProgram()
            self.server()

    def start_channel(self):
        msg=rqst_forTimeSchedule+f':{self.number}'
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
            soc.connect((host,port))
            soc.sendall(msg.encode(format))
            while True:
                recv=soc.recv(txt_messageSize).decode(format)
                if  recv==msg_receiving : 
                    recv=f"channel {self.number} => "+msg_receivingTimeSchedule
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
            self.port=int(self.data['port'])
            self.timing=self.data['programs']
            print(f'host:{self.host}\nport:{self.port}\ntiming:{self.timing}')
            '''return value'''
            ret=True
        except:
            '''if self.data does not include json file'''
            '''return value'''
            ret=False
        self.data=[]

        return ret
    
    def receive_liveProgram(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
            '''bind each channel to main server'''
            soc.connect((host, port))
            '''create special msg for each channel'''
            msg=rqst_forImg+f':{self.number}'
            soc.sendall(msg.encode(format))
            '''wating for receiving images from main server'''
            while True:
                recv=soc.recv(img_messageSize).decode(format)
                if  recv==msg_receiving : 
                    recv=f"channel {self.number} => "+msg_receivingImgs
                    break
                else:
                    self.data.append(recv)
            print(recv)
        '''reconstruct incoming data by connecting packets'''
        self.programs_json="".join(self.data)
        self.programs_dict=json.loads(self.programs_json)


    
    def server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM,socket.IPPROTO_UDP) as soc:
            self.multicast_group=(self.host, self.port)
            # soc.settimeout(0.2)
            ttl=struct.pack('b', self.ttl)
            soc.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
            # soc.sendto(f"channel number {self.number} is ready\n\n".encode(format),self.multicast_group)
            while True:
                for img in self.programs_dict['live']['imgs']:
                    packet=json.dumps(img)
                    packet=packet.encode(format)
                    soc.sendto(packet,self.multicast_group)

                    

def init():
    network=[]
    for i in range(1,4):
        net=Network(i)
        net.start()
        network.append(net)

    for i in range(3):
        network[i].join()        



if __name__=='__main__':
    init()
  
    