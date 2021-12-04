import json
import socket
import base64
from numpy import infty
from client_constants import *
import time
import struct

class Network:
    def __init__(self,id):
        self.id = id
        self.data = []
        self.get_ipPort()
    

    def get_ipPort(self):
        msg=rqst_forIpPort+f':{self.id}'
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
            soc.connect((host,port))
            soc.sendall(msg.encode(format))
            while True:
                recv = soc.recv(txt_messageSize).decode(format)
                if  recv==msg_receiving : 
                    recv=msg_receivingIpPort
                    break
                else:
                    self.data.append(recv)
        print(recv)
        self.channels_ipPort="".join(self.data)
        self.channels_ipPort=json.loads(self.channels_ipPort)
        self.channels_ipPort={item['number']:{'host':item['host'], 'port':item['port'], 'timing':json.loads(item['timing'])} for item in self.channels_ipPort}
        print(f"channels are ready")
        self.data=[]

    def receive_data(self,channel):
        multicast_group=self.channels_ipPort[channel]['host']
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM,socket.IPPROTO_UDP) as soc:

            soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            soc.bind(("",int(self.channels_ipPort[channel]['port'])))
            group = socket.inet_aton(multicast_group)
            mreq = struct.pack('4sL', group, socket.INADDR_ANY)
            soc.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

            images=[]
            packet,addr=soc.recvfrom(img_messageSize)
            packet=packet.decode(format)
            packet=json.loads(packet)
            start=int(packet['num'])
            index=int(packet['num'])
            state=float('inf')
            
            while state != start:
                image={
                    'num':index,
                    'img':[],
                }
                state=index
                while state==index:
                    image['img'].append(packet['img'])
                    packet,addr=soc.recvfrom(img_messageSize)
                    packet=packet.decode(format)
                    packet=json.loads(packet)
                    index=int(packet['num'])
                state=index

                image['img']="".join(image['img'])
                images.append(image)
                # print(start,index,state)
            images=images[1:]
            for img in images:

                num=img['num']
                temp=img['img']
                temp=temp.encode(format)
                temp=base64.decodebytes(temp)
                with open(f'cache/index{num}.png','wb') as im:
                    im.write(temp)

            

    

if __name__ == "__main__":
    network=Network(1)
    network.receive_data('1')
