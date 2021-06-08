import os
import cv2
import json
from pandas.core.base import PandasObject
import rawpy
import pickle
import numpy as np
import pandas as pd
from typing import *
import face_recognition

def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
	dim = None
	(h, w) = image.shape[:2]
	if width is None and height is None:
		return image
	if width is None:
		r = height / float(h)
		dim = (int(w * r), height)
	else:
		r = width / float(w)
		dim = (width, int(h * r))
	resized = cv2.resize(image, dim, interpolation = inter)
	return resized

def process(img: np.ndarray, known_face_names: List, known_face_encodings: np.ndarray) -> List:
    '''
    img: rgb image
    '''
    face_locations = face_recognition.face_locations(img)
    face_encodings = face_recognition.face_encodings(img, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = None

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        face_names.append(name)

    return face_names

def mapper(name: str) -> PandasObject:
    for f in os.listdir('csv_classes'):
        df = pd.read_csv(os.path.join('csv_classes', f), encoding='utf-16')
        
        for i in df.itertuples():
            if '_'.join(i._5.replace('\\', '/').split('/')[-2:]) == name:
                return i

with open('dataset_faces.dat', 'rb') as f:
    all_face_encodings = pickle.load(f)

known_face_names = list(all_face_encodings.keys())
known_face_encodings = np.array(list(all_face_encodings.values()))

output = dict()

root = "F:/magic/Documents/SESC_STUDENTS"

for i in os.listdir(root):
    for j in os.listdir(os.path.join(root, i)):
        path = os.path.join(root, i, j)
        if not(os.path.isfile(path)): continue

        if path.lower().endswith('cr2'):
            img = rawpy.imread(path).postprocess()
        elif path.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            img = cv2.imread(path)
            img = img[:, :, ::-1]
        else:
            continue

        img = image_resize(img, width=1000)

        try:
            name = process(img, known_face_names, known_face_encodings)[0]
        except:
            name = None
        
        output[path] = name

        print("[INFO] " + str(os.listdir(os.path.join(root, i)).index(j) + 1) + "/" + str(len(os.listdir(os.path.join(root, i)))))
    print("!!! [INFO] " + str(os.listdir(root).index(i) + 1) + "/" + str(len(os.listdir(root))))

for key in output:
    if output[key] is not None:
        temp = mapper(output[key])
        output[key] = {
            'name': temp._1,
            'group': int(temp.Группа),
            'bday': temp._3,
            'icon': temp._5
        }
    else:
        output[key] = {
            'name': None,
            'group': None,
            'bday': None,
            'icon': None
        }

with open('output.json', 'w', encoding='utf-16') as f:
    json.dump(output, f, indent=4, ensure_ascii=False)