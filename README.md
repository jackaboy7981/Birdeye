# Blind Spot Monitoring System through real time Birdseye view render
An AI Capable of 3d Object detection and an UI that reders the detected objects into birdseye view is developed.
<p align="center"><img src="AI/assets/Dashboard.jpeg" width="720"\></p>

The Dataset used : https://www.nuscenes.org

Sensor suit and camera coverage in the dataset
<p align="center"><img src="AI/assets/sensor.png" width="720"\></p><p align="center"><img src="AI/assets/coverage.jpg" width="500"\></p>
Input from Dataset and System Output:
<p align="center" align="center"><img src="AI/assets/Combined-explanation.gif" width="720"\></p>
<p align="center"><img src="AI/assets/combined.gif" width="720"\></p>

# Index
->AI Sample Outputs<br>
->System Overview<br>
->Repo Layout

# AI Sample Outputs:
AI input output mapping:
<p align="center"><img src="AI/assets/input-output.jpg" width="720"\></p>
Sample Predictions:
<p align="center"><img src="AI/assets/266.gif" width="720"\></p>
<p align="center"><img src="AI/assets/260.gif" width="720"\></p>
<p align="center"><img src="AI/assets/265.gif" width="720"\></p>
more ai sample outputs from the test dataset can be found in the AI/assets folder

# System Overview
<p align="center"><img src="AI/assets/Systemoverview.png" width="720"\></p>
AI Model Architecture :<br>
The AI model uses a Modified Yolo v3 in which the six images from the 6 cameras is feed through 6 different feature extraction networks(Darknet) and the output from these feature extraction networks are stacked back to back and feed to a object detector which instead of just predicting the x,y, l,w ,conf and category like the usual yolo network , it predicts x,y,z h,w,l, r1,r2 conf, category where z is the z coordinate of the centroid, h for the height of the object and r1,r2 for the orientation of the object where r1 is the sine and r2 is the cosine of the original orientation.
<p>The images used for traing the model was of size 416x416 and was predicting objects in a 13 meter radius</p>

# Repo Layout
<p>The code for the AI model is present in the AI/Birdnet_Yolo.ipynb python notebook and the configuration file in the AI/config/birdnet-yolo.cfg</p>
<p>Trained weight for the AI model can be found in the AI/weights folder</p>
