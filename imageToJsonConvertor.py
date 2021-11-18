import json
import base64
from glob import glob


def sortPath(path):
    split_path=path.split('\\')
    number=split_path[len(split_path)-1].split('.')[0]
    return int(number)

def convertor(file_path,data):
    file_name=file_path.split('\\')[1]
    data[file_name]=[]
    image_paths=glob(f"{file_path}\/\//*")

    """sort paths by the image index number"""
    image_paths.sort(key=sortPath)

    for image_path in image_paths:
        with open(image_path, mode='rb') as img:
            binary_img = img.read()
            encoded_img = base64.encodebytes(binary_img).decode('utf-8')
            data[file_name].append(encoded_img)

def start():
    #for saveing images
    data={}
    file_paths=glob("save/*")
    for file_path in file_paths:
        convertor(file_path,data)
    
    json_images=json.dumps(data)
    return json_images

    
if __name__ == "__main__":
    start()