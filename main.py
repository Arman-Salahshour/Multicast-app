from fastapi import FastAPI
from pydantic import BaseModel
import threading
import multiprocessing
import json
import server
import client
import time


class User(BaseModel):
    id: str
    channel: int

app=FastAPI()
@app.post('/start/')
async def get_img(user:User):
    try:
        process=multiprocessing.Process(target=client.init, args=(user.id,user.channel,))
        process.start()
        process.join()
        msg=f'Frames has saved'
    except Exception as e:
        msg=f'Frames has not saved'

    return {'msg':msg}



if __name__ == '__main__':
    mainServer=multiprocessing.Process(target=server.init, args=('main',))
    mainServer.start()
