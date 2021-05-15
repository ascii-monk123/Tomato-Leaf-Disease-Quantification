import cv2
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
# from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go

imgNo=41
imgPath='/home/aahan/Documents/Minor Project/Tomato Early Blight/EB{}.jpg'.format(imgNo)

image=cv2.cvtColor(cv2.imread(imgPath),cv2.COLOR_BGR2RGB)

r,g,b=cv2.split(image)

r,g,b=(r.flatten(),g.flatten(),b.flatten())

marker_data=go.Scatter3d(x=r,y=g,z=b,marker=go.scatter3d.Marker(size=3),opacity=0.8,mode='markers')
figure=go.Figure(data=marker_data)
figure.show()