import frameConvertor
import imageToJsonConvertor
import json
from datetime import datetime
import socket
from constants import *
import time
import pandas as pd
import random
import numpy as np
from _thread import *
import threading

class Network:
    def __init__(self,host,port,chanels,data,keys,win):
        self.host = host
        self.port = port
        self.chanels = chanels
        self.data = data
        self.keys = keys
        self.win=win
        self.lock=threading.Lock()

    def get_livePrograms(self,):
        
        """extract movies schedule and live movie {name , size , imgs}"""
        programs=check_movieTime(self.data)
        movies=programs['movies']
        live_movieName=programs['live']['name']
        live_movieSize=programs['live']['size']
        live_movieImgs=programs['live']['imgs']
        self.lock.release()
        return movies, live_movieName, live_movieSize, live_movieImgs

    def sending_liveProgram(self,conn):
        movies, live_movieName, live_movieSize, live_movieImgs=self.get_livePrograms()
        """step 1 sending movies' schedule"""
        json_movies=json.dumps(movies).encode(format)
        conn.sendall(json_movies)
        conn.sendall(end_moviesMsg.encode(format))

        """step 2 sending live movie name"""
        json_liveMovieName=json.dumps(live_movieName).encode(format)
        conn.sendall(json_liveMovieName)
        conn.sendall(end_liveMovieNameMsg.encode(format))

        """step 3 sending live movie size"""
        json_liveMovieSize=json.dumps(live_movieSize).encode(format)
        conn.sendall(json_liveMovieSize)
        conn.sendall(end_liveMovieSizeMsg.encode(format))

        """step 4 sending live movie imgs"""
        # for img in live_movieImgs:
        #     json_img=json.dumps(img)
            
        

        # for item in programs['live']['imgs']:
        #     # time.sleep(2)
        #     # json_programs=json.dumps({'data':programs['live']['imgs'][0]})
        #     json_programs=json.dumps({'data':item})
        #     win=100
        #     for line in range(0,len(json_programs),win):
        #         sending=json_programs[line:line+win]
        #         conn.sendall(sending.encode('utf8'))
        #     # conn.sendall(json_programs.encode(format))
        time.sleep(2)
        conn.sendall(end_sendingMsg.encode(format))
        print('Sending has done')
    
        # print(len(msg))
        # splitn=100
        # for line in range(0,len(msg),splitn):
        #     sending=msg[line:line+splitn]
        #     conn.sendall(sending.encode('utf8'))
        # conn.sendall(endSending.encode('utf8'))
        # programs=check_movieTime(data)
        # json_programs=json.dumps(programs,ident=4)
        # conn.sendall(json_programs.encode(format))
        # print('Sending has done')

    def connection_toClient(self,conn,addr,):
            self.lock.acquire()
            self.data = setTime(self.data,self.keys)
            
            with conn:
                    print(f"server is connected to {addr[0]}:{addr[1]}")
                    while True:
                        recv_data=conn.recv(txt_messageSize).decode(format)
                        if not recv_data: 
                            break
                        elif recv_data==rqst_forImg:
                            self.sending_liveProgram(conn)
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
        if hour >= h1 or hour < h2:
            programs['live']['name']=key
            programs['live']['size']=data[key]['size']
            programs['live']['imgs']=data[key]['imgs']
    return programs

def get_chanelFrame(data):
    chanels=pd.DataFrame({
        'chanel':[],
        'host':[],
        'port':[],
    })
    
    for i in range(4):
        ip=host.split('.')
        ip[len(ip)-1]=str(int(ip[len(ip)-1])+i+1)
        ip=".".join(ip)
        df={
        'chanel':f"{i+1}",
        'host':ip,
        'port':port,
        }
        chanels=chanels.append(df,ignore_index=True)
    return chanels






def init():
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
    '''define ip/port for each chanel'''
    chanels=get_chanelFrame(json_movieImgDict)
    '''create an object for network'''
    network=Network(host=host,port=port,chanels=chanels,data=json_movieImgDict,keys=movies_name,win=100)
    '''run server to accept chanels' client side request'''
    network.serverProtocol()





if __name__ == "__main__":
    '''initialize server settings'''
    init()