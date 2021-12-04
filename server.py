import channel
import frameConvertor
import imageToJsonConvertor
import json
from datetime import datetime
import socket
from server_constants import *
import time
import pandas as pd
import random
import numpy as np
import threading
import copy
import warnings
warnings.filterwarnings("ignore")

class Network:
    def __init__(self,name,host,port,channels,data,keys,win):
        self.name = name
        self.host = host
        self.port = port
        self.channels = channels
        self.data = data
        self.keys = keys
        self.win=win
        self.lock=threading.Lock()

    def get_livePrograms(self,data):
        
        """extract movies schedule and live movie {name , size , imgs}"""
        programs=check_movieTime(data)
        movies=programs['movies']
        live_movieName=programs['live']['name']
        live_movieSize=programs['live']['size']
        live_movieImgs=programs['live']['imgs']
        # self.lock.release()
        return programs,movies, live_movieName, live_movieSize, live_movieImgs


    def connection_toClient(self,conn,addr,):
            
            with conn:
                    print(f"server is connected to {addr[0]}:{addr[1]}")
                    while True:
                        recv_data=conn.recv(txt_messageSize).decode(format).split(':')
                        applicant=recv_data[0]
                        
                        '''if a channel send message'''
                        if(applicant=='channel'):
                            self.lock.acquire()
                            '''split the channel msg and number of channel'''
                            msg=recv_data[1]
                            channel=recv_data[2]
                            '''if a channel wants to run itself, it will send this message to receive ip,port for server side of itself and programs' schedule time'''
                            if msg==rqst_forTimeSchedule:
                                '''if the channel is not active, the config file will be sent for the channel'''
                                if (self.channels['active'][self.channels['number']==channel].values[0]==False):
                                    self.channels['active'].loc[self.channels['number']==channel]=True
                                    '''setTime function sets time for movies, specifically for each channel'''
                                    channelData=setTime(copy.deepcopy(self.data),self.keys)
                                    
                                    '''set data in channels data frame'''
                                    self.channels['data'].loc[self.channels['number']==channel]=json.dumps(channelData)
                                    
                                    '''get movies' schedule time'''
                                    programs=self.get_livePrograms(channelData)[0]['movies']

                                    '''set channels schedule time'''
                                    self.channels['timing'].loc[self.channels['number']==channel]=json.dumps(programs)

                                    '''create channel's config dictionary'''
                                    config={
                                        'ip':self.channels['host'].loc[self.channels['number']==channel].values[0],
                                        'port':self.channels['port'].loc[self.channels['number']==channel].values[0],
                                        'programs':programs
                                    }
                                    
                                    '''convert it to json file'''
                                    config=json.dumps(config)
                                    '''send config file'''
                                    conn.sendall(config.encode(format))
                                    time.sleep(0.5)
                                    conn.sendall(end_sending.encode(format))

                                    '''release thread lock'''
                                    self.lock.release()
                                    break
                                else:
                                    '''if the channel is active this block will be active'''
                                    '''release thread lock'''
                                    self.lock.release()
                                    '''send a message for notice that this channel is active'''
                                    conn.sendall(msg_active.encode(format))
                                    time.sleep(0.5)
                                    break
                            
                            
                            elif msg==rqst_forImg:
                                '''for sending images of live program'''
                                channelData=self.channels['data'].loc[self.channels['number']==channel].values[0]

                                '''convert json data to dictionary'''
                                channelData=json.loads(channelData)

                                '''get live program's images'''
                                programs=self.get_livePrograms(channelData)[0]

                                '''convert images to json file'''
                                programs=json.dumps(programs)

                                '''send json images'''
                                conn.sendall(programs.encode(format))
                                time.sleep(0.5)
                                conn.sendall(end_sending.encode(format))
                                print('Sending images has done')
                                '''release thread lock'''
                                self.lock.release()
                                break

                        elif applicant=='client':
                            msg=recv_data[1]
                            client_id=recv_data[2]
                            if msg==rqst_forIpPort:
                                channels_ipPort=self.channels[['number','host','port','timing']].to_json(orient='records')
                                conn.sendall(channels_ipPort.encode(format))
                                time.sleep(0.25)
                                conn.sendall(end_sending.encode(format))
                                print(f'Sending channels\' ip port to client {client_id}')
                            break


                        if not recv_data: 
                            break
                        else:
                            pass



    def serverProtocol(self):
        '''initilize socket networking (server side) '''
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()

            while True:
                conn,addr=s.accept()
                connection=threading.Thread(target=self.connection_toClient,args=(conn,addr,))
                connection.start()
                connection.join()
                print(f"{addr[0]}:{addr[1]} is disconnected")


        




def setTime(data,keys):
    random.shuffle(keys)
    hours = 24 
    length = int(hours/len(data))
    time=0
    for key in keys:
        data[key]['hour']=f"{time}_{time+length}"
        time+=length
    return data

    
def getTime():
    time=datetime.now()
    hour=time.hour
    return hour

def check_movieTime(data):
    hour = getTime()
    programs={'movies':{},'live':{}}
    for key in data:
        time=data[key]['hour']
        programs['movies'][key]=time
        h1,h2=time.split('_')
        h1,h2=(int(h1),int(h2))
        if hour >= h1 and hour < h2:
            programs['live']['name']=key
            programs['live']['size']=data[key]['size']
            programs['live']['imgs']=data[key]['imgs']

    
    return programs

def get_channelFrame(num):
    channels=pd.DataFrame({
        'number':[],
        'host':[],
        'port':[],
        'data':[],
        'active':[],
        'timing':[]

    })
    
    for i in range(num):
        ip=multicast_groupIP.split('.')
        ip[len(ip)-1]=str(int(ip[len(ip)-1])+i+1)
        ip=".".join(ip)
        port=multicast_groupPort+i
        df={
        'number':f"{i+1}",
        'host':ip,
        'port':port,
        'active':False,
        }
        channels=channels.append(df,ignore_index=True)
    return channels






def init(name):
    '''extract frames from movies'''
    # frameConvertor.start(number=200,gap=5)
    '''convert frames and movies' description to json'''
    json_movieImg=imageToJsonConvertor.start()
    '''convert json to dictionary'''
    json_movieImgDict=json.loads(json_movieImg)
    '''extract movies' name'''
    movies_name=[i for i in json_movieImgDict.keys()]
    '''set clock for stream for each movie'''
    json_movieImgDict=setTime(json_movieImgDict,movies_name)
    '''define ip/port for each channel'''
    channels=get_channelFrame(3)
    '''create an object for network'''
    network=Network(name=name,host=host,port=port,channels=channels,data=json_movieImgDict,keys=movies_name,win=100)
    '''run server to accept channels' client side request'''
    serverProtocol=threading.Thread(target=network.serverProtocol)
    '''run server to get images from server and clients' request'''
    runChannel=threading.Thread(target=channel.init)
    serverProtocol.start()
    runChannel.start()
    serverProtocol.join()
    runChannel.join()
    






if __name__ == "__main__":
    '''initialize server settings'''
    init()