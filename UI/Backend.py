import time
import math
#from nuscenes.nuscenes import NuScenes 
import json
import numpy as np
from pyquaternion import Quaternion

import communications
commu = communications.communications()

#seting up socket
host, port = "127.0.0.1", 54955

#nusc = NuScenes(version='v1.0-mini', dataroot='data', verbose=True)

max_height=5
max_length=20
max_width=20

def quaternion_to_euler_angle_vectorized2(w, x, y, z):
    ysqr = y * y

    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + ysqr)
    X = np.degrees(np.arctan2(t0, t1))

    t2 = +2.0 * (w * y - z * x)

    t2 = np.clip(t2, a_min=-1.0, a_max=1.0)
    Y = np.degrees(np.arcsin(t2))

    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (ysqr + z * z)
    Z = np.degrees(np.arctan2(t3, t4))

    return X, Y, Z

def rotate_around_point_lowperf(point, radians, origin=(0, 0)):
      """Rotate a point around a given point.
      
      I call this the "low performance" version since it's recalculating
      the same values more than once [cos(radians), sin(radians), x-ox, y-oy).
      It's more readable than the next function, though.
      """
      x, y = point
      ox, oy = origin

      qx = ox + math.cos(radians) * (x - ox) + math.sin(radians) * (y - oy)
      qy = oy + -math.sin(radians) * (x - ox) + math.cos(radians) * (y - oy)

      return qx, qy

def quaternion_yaw(q: Quaternion) -> float:
      """
      Calculate the yaw angle from a quaternion.
      See https://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles.
      :param q: Quaternion of interest.
      :return: Yaw angle in radians.
      """

      a = 2.0 * (q[0] * q[3] + q[1] * q[2])
      b = 1.0 - 2.0 * (q[2] ** 2 + q[3] ** 2)

      return np.arctan2(a, b)

def convert_to_top_corner(point):
      """Convert the position with respect to the top left corner"""
      point[0] = max_length + point[0]
      point[1] = max_width - point[1]
      return point


with open('data/combined_samples.json') as f:
    samples = json.load(f)
for i in range(394):
    ego_pose = samples[i]['ego_pose']
    #sock.sendall("FRAME".encode("UTF-8"))
    commu.send_scn_end()
    annos_list = []
    #ToSendString = ""
    for annos in samples[i]['anns']:
        annotation_metadata =  annos
        
        ego_yaw = quaternion_yaw(ego_pose['rotation']) - math.pi/2
        cordinates = [annotation_metadata['translation'][i] - ego_pose['translation'][i] for i in range(3)]
        cordinates[0], cordinates[1] = rotate_around_point_lowperf(cordinates[:2], ego_yaw, origin=(0, 0))
        #cordinates = convert_to_top_corner(cordinates)
        if cordinates[0] > max_width or cordinates[0] < - max_width or cordinates[1] > max_length or cordinates[1] < -max_length:# or (self.augment and self.check_cameraregion() == 0):
            continue

        #rotation = [annotation_metadata['rotation'][i] - ego_pose['rotation'][i] for i in range(4)]
        #rotation = [0,0,0,0]
        rotation = [0, 0, 0]
        rotation[0], rotation[1], rotation[2] = quaternion_to_euler_angle_vectorized2(annotation_metadata['rotation'][0], annotation_metadata['rotation'][1], annotation_metadata['rotation'][2], annotation_metadata['rotation'][3])
        ego_angle = [0, 0 ,0]
        ego_angle[0], ego_angle[1], ego_angle[2] = quaternion_to_euler_angle_vectorized2(ego_pose['rotation'][0], ego_pose['rotation'][1], ego_pose['rotation'][2], ego_pose['rotation'][3])
        rotation = [ego_angle[i] - rotation[i] for i in range(3)]

        anno_dict = {'translation':cordinates, 'size': annotation_metadata['size'], 'rotation': rotation, 'category_name':annotation_metadata['category_name']}
        annos_list.append(anno_dict)
        '''
        #converting list to string then to byte and sending to c#
        transString = ','.join(map(str, cordinates)) #Converting translation list to a string, example "0,0,0"
        sizeString = ','.join(map(str, annotation_metadata['size'])) #Converting size list to a string, example "0,0,0"
        rotationString = ','.join(map(str, rotation)) #Converting rotation list to a string, example "0,0,0"
        
        #concatenate every annotations in a scene into a single string
        ToSendString = ToSendString + "$" + sizeString + "/" + rotationString + "/" + annotation_metadata['category_name'] + "/" + transString

        print(rotation)
        '''
    #sock.sendall(ToSendString.encode("UTF-8"))
    sample_dict = {'anns':annos_list}
    commu.send_sample(sample_dict)
    time.sleep(0.5) #sleep 0.5 sec
    #sock.sendall("DONE".encode("UTF-8")) #please delete this for final testing
    #break #use this break while testing
    #sock.sendall("SCENE".encode("UTF-8"))
#sock.sendall("DONE".encode("UTF-8"))
#sock.close()