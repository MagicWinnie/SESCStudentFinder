import os
import cv2
import json
import rawpy
import pickle
import numpy as np
import pandas as pd
from typing import *
import face_recognition

name = "10-1_18.png"
flag = False

for f in os.listdir('csv_classes'):
    if flag: break

    df = pd.read_csv(os.path.join('csv_classes', f), encoding='utf-16')
    
    for i in df.itertuples():
        if '_'.join(i._5.replace('\\', '/').split('/')[-2:]) == name:
            flag = True
            print(i.Группа)
            break