import frameConvertor
import imageToJsonConvertor
import json
from datetime import datetime
from socket import socket
from constants import *

# class Network:
#     def __init__(self,host,port):
#         self.host = host
#         self.port = port
    
#     def server(self):
#         with socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#             s.bind((self.host, self.port))
#             s.listen()
#             conn,addr=s.accept()
#             with conn:
#                 print(f"server is connected to {addr}")
#                 while True:
#                     data=conn.recv(size).encode(format)
#                     if not data: 
#                         break





def setTime(data):
    hours = 24 
    length = int(hours/len(data))
    time=0
    for key in data:
        data[key]['hour']=f"{time}_{time+length}"
        time+=length+1

    
def getTime():
    time=datetime.now()
    hour=time.hour
    print(hour)
    


def init():
    # frameConvertor.start(number=200,gap=5)
    json_img=imageToJsonConvertor.start()
    json_imgDict=json.loads(json_img)
    setTime(json_imgDict)
    print(json_imgDict['LookUp']['hour'])
    getTime()





if __name__ == "__main__":
    init()