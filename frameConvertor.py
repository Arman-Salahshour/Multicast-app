import os
import numpy as np  
from glob import glob
import cv2   
import imutils  


def make_dir(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError:
        print (f"Could not create directory with '{path}' name")

def save_frame(video_path,save_dir,number=1000,gap=10):
    """initialize a path for saving frames"""
    name=video_path.split('\\')[1].split('.')[0]
    save_path=os.path.join(save_dir,name)
    make_dir(save_path)
    
    """take frames from the video"""
    cap=cv2.VideoCapture(video_path)
    #index of the frame
    index=0
    while index <= number:
        ret,frame=cap.read()
        if ret == False: 
            cap.release()
            break
        #determine frames resolution
        frame=imutils.resize(frame,width=720)
        if index == 0:
            cv2.imwrite(f"{save_path}/{index}.png",frame)
        elif index % gap == 0:
            cv2.imwrite(f"{save_path}/{index}.png",frame)
        index += 1




def start(number=100,gap=10):
    video_paths=glob("videos/*")
    save_dir="save"
    for path in video_paths:
        save_frame(path,save_dir,number=number,gap=gap)

if __name__ == '__main__':
    start(number=400,gap=2)