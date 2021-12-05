from os import error
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
        data=client.init(user.id,user.channel)
        """make a process for each client to recieve images"""
        process=multiprocessing.Process(target=data['recieveData'], args=(f'{user.channel}',))
        process.start()
        process.join()
        msg=f'Frames have saved'

        return {
            'msg':msg,
            'timing':data['timing'],
        }
    except Exception as e:
        msg=f'Frames have not saved'
        return {'msg':msg}



if __name__ == '__main__':
    '''make a process for running server and channels'''
    mainServer=multiprocessing.Process(target=server.init, args=('main',))
    mainServer.start()
