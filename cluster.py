# import the necessary packages
from imutils import build_montages
#from pathlib import Path
import numpy as np
#import argparse
import pickle
import cv2
import glob
from os import path
import sys
import dlib
import ffrsettings
import collections

settings = ffrsettings.ffrsettings()

THRESHOLD = float(sys.argv[1])
#settings.threshold
#CLUSTER_IMAGE_DIR = settings.resultsdir
PICKLES_DIR = settings.encodingsdir
#IMG_DIR = settings.imgdir

#start = int(sys.argv[2])
#end = int(sys.argv[3])

# load the serialized face encodings + bounding box locations from
# disk, then extract the set of encodings to so we can cluster on
# them
print("[INFO] loading encodings...")

data = []

files = glob.glob(path.join(PICKLES_DIR, '*.pickle'))
print(len(files))

for picklefile in files:
    d = pickle.loads(open(picklefile, "rb").read())
    data.extend(d)

#data = pickle.loads(open(args["encodings"], "rb").read())
#data = np.array(data)
print(len(data))
encodings = [dlib.vector(d["encoding"]) for d in data]
#[start:end]]
print(len(encodings))
#print(type(encodings))
#print(encodings[0])

# cluster the embeddings
print("[INFO] clustering...")
#clt = DBSCAN(metric="euclidean", n_jobs=-1)
#clt.fit(encodings)

labels = dlib.chinese_whispers_clustering(encodings, THRESHOLD)

tup = (data, labels)

pickleFile = 'clusters-%.3f.pickle' % THRESHOLD

with open(pickleFile, "wb") as f:
    f.write(pickle.dumps(tup))

