import json
import socket
from client_constants import *
import time

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
        self.channels_ipPort={item['number']:{'host':item['host'], 'port':item['port']} for item in self.channels_ipPort}
        print(f"channels: {self.channels_ipPort}")
        self.data=[]











if __name__ == "__main__":
    network=Network(1)
