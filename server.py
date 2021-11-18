import frameConvertor
import imageToJsonConvertor

class Server:
    def __init__(self):
        pass


def init():
    frameConvertor.start(number=1000,gap=10)
    json_img=imageToJsonConvertor.start()



if __name__ == "__main__":
    init()