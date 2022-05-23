import socket
from pyquaternion import Quaternion
import math
import numpy as np

class communications:
    def __init__(self, host="127.0.0.1", port= 54955, max_height=5, max_length=20, max_width=20) -> None:
        
        self.max_height=max_height
        self.max_length=max_length
        self.max_width=max_width
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

    def send_sample(self, sample) -> None:
        ToSendString = ""
        for annotation_metadata in sample['anns']:
            #converting list to string then to byte and sending to c#
            transString = ','.join(map(str, annotation_metadata['translation'])) #Converting translation list to a string, example "0,0,0"
            sizeString = ','.join(map(str, annotation_metadata['size'])) #Converting size list to a string, example "0,0,0"
            rotationString = ','.join(map(str, annotation_metadata['rotation'])) #Converting rotation list to a string, example "0,0,0"
            
            #concatenate every annotations in a scene into a single string
            ToSendString = ToSendString + "$" + sizeString + "/" + rotationString + "/" + annotation_metadata['category_name'] + "/" + transString

        #print(ToSendString)
        self.sock.sendall(ToSendString.encode("UTF-8"))

    def send_scn_end(self) -> None:
        self.sock.sendall("FRAME".encode("UTF-8"))

    def teardown(self):
        self.sock.sendall("DONE".encode("UTF-8"))
        self.sock.close()