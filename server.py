import frameConvertor
import imageToJsonConvertor
import json
from datetime import datetime
import socket
from constants import *
import time
import pandas as pd





def setTime(data):
    hours = 24 
    length = int(hours/len(data))
    time=0
    for key in data:
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
        'movie':[],
        'chanel':[],
        'host':[],
        'port':[],
    })

    for key in data:
        df={
        'movie':key,
        'chanel':"",
        'host':"",
        'port':"",
        }
        chanels=chanels.append(df,ignore_index=True)
    return chanels






def init():
    # frameConvertor.start(number=200,gap=5)
    json_movieImg=imageToJsonConvertor.start()
    json_movieImgDict=json.loads(json_movieImg)
    json_movieImgDict=setTime(json_movieImgDict)
    chanels=get_chanelFrame(json_movieImgDict)
    # network=Network(host=host,port=port,data=json_imgDict,win=100)
    # network.serverProtocol()





if __name__ == "__main__":
    init()