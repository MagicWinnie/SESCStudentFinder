import os
import sys
import pickle
import numpy as np
import face_recognition
import cv2

all_face_encondings = {}

args = sys.argv

if len(args) != 2:
    print("Usage: python scraping_images.py path/to/saved/icons")
    exit(-1)

root = args[-1]

files = os.listdir(root)

for i in files:
    tmp = os.listdir(os.path.join(root, i))
    for j in tmp:
        try:
            all_face_encondings[i + '_' + j] = face_recognition.face_encodings(cv2.imread(os.path.join(root, i, j)))[0]
        except IndexError:
            print("[ERROR] " + i + '_' + j)
        print("[INFO] " + str(tmp.index(j) + 1) + "/" + str(len(tmp)))
    print("[INFO] " + str(files.index(i) + 1) + "/" + str(len(files)))

with open('dataset_faces.dat', 'wb') as f:
    pickle.dump(all_face_encondings, f)
