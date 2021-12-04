import json
import base64
import os
from glob import glob


def sortPath(path):
    split_path=path.split('\\')
    number=split_path[len(split_path)-1].split('.')[0]
    return int(number)

def convertor(file_path,data,win):
    file_name=file_path.split('\\')[1]
    size=os.path.getsize(file_path)

    data[file_name]={'size':size, 'imgs':[]}
    image_paths=glob(f"{file_path}\/\//*")

    """sort paths by the image index number"""
    image_paths.sort(key=sortPath)
    for image_path in enumerate(image_paths):
        with open(image_path[1], mode='rb') as img:
            binary_img = img.read()
            encoded_img = base64.encodebytes(binary_img).decode('utf-8')
            '''make packets from image'''
            for line in range(0,len(encoded_img),win):
                partial_img=encoded_img[line:line+win]
                packet={'num':image_path[0],
                        'img':partial_img}
                data[file_name]['imgs'].append(packet)
            

def start(win=4096):
    #for saveing images
    data={}
    file_paths=glob("save/*")
    for file_path in file_paths:
        convertor(file_path,data,win)
        
    json_images=json.dumps(data)
    return json_images

    
if __name__ == "__main__":
    start(win=4096)

    # encoded_img = base64.encodebytes(binary_img)
    # en=struct.pack('Q',len(encoded_img))+encoded_img
    # print(en)