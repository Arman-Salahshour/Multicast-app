from fastapi import FastAPI
from pydantic import BaseModel
import multiprocessing
import server
import client


"""A class as a model for data which recieve from post request"""
class User(BaseModel):
    id: str
    channel: int
'''Start using fast api'''
app=FastAPI()
@app.post('/start/')
async def get_img(user:User):
    try:
        """make a process for each client"""
        process=multiprocessing.Process(target=client.init, args=(user.id,user.channel,))
        process.start()
        process.join()
        msg=f'Frames has saved'
    except Exception as e:
        msg=f'Frames has not saved'

    return {'msg':msg}



if __name__ == '__main__':
    '''make a process for running server and channels'''
    mainServer=multiprocessing.Process(target=server.init, args=('main',))
    mainServer.start()
