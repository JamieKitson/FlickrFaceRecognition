# import the necessary packages
#from sklearn.cluster import DBSCAN
from imutils import build_montages
from pathlib import Path
import numpy as np
import argparse
import pickle
import cv2
import glob
import os
import sys
import dlib
import ffrsettings

settings = ffrsettings.ffrsettings()

THRESHOLD = settings.threshold
CLUSTER_IMAGE_DIR = settings.resultsdir
PICKLES_DIR = settings.encodingsdir

start = int(sys.argv[1])
end = int(sys.argv[2])


# load the serialized face encodings + bounding box locations from
# disk, then extract the set of encodings to so we can cluster on
# them
print("[INFO] loading encodings...")

data = []

files = glob.glob(os.path.join(PICKLES_DIR, '*.pickle'))
print(len(files))

for picklefile in files:
	d = pickle.loads(open(picklefile, "rb").read())
	data.extend(d)

#data = pickle.loads(open(args["encodings"], "rb").read())
#data = np.array(data)
print(len(data))
encodings = [dlib.vector(d["encoding"]) for d in data[start:end]]
print(len(encodings))
#print(type(encodings))
#print(encodings[0])

# cluster the embeddings
print("[INFO] clustering...")
#clt = DBSCAN(metric="euclidean", n_jobs=-1)
#clt.fit(encodings)

labels = dlib.chinese_whispers_clustering(encodings, THRESHOLD)

# determine the total number of unique faces found in the dataset
labelIDs = np.unique(labels)

#withCounts = np.unique(labels, return_counts=True)

#print(withCounts[1])
#print(type(withCounts[1]))
#labelIDs = withCounts[0].argsort(withCounts[1].astype(np.int64))
#print(labelIDs)

numUniqueFaces = len(np.where(labelIDs > -1)[0])
print("[INFO] # unique faces: {}".format(numUniqueFaces))

# loop over the unique face integers
for labelID in labelIDs:
	# find all indexes into the `data` array that belong to the
	# current label ID, then randomly sample a maximum of 25 indexes
	# from the set
	print("[INFO] faces for face ID: {}".format(labelID))
	idxs = np.where(labels == labelID)[0]
	c = len(idxs)
	if c < 4:
		continue
	idxs = np.random.choice(idxs, size=min(81, len(idxs)),
		replace=False)

	# initialize the list of faces to include in the montage
	faces = []

	# loop over the sampled indexes
	for i in idxs:
		#print(data[i])
		# load the input image and extract the face ROI
		image = cv2.imread(os.path.join('img', data[i]["photoId"] + '.jpg'))
		(top, right, bottom, left) = data[i]["loc"]
		face = image[top:bottom, left:right]

		# force resize the face ROI to 96x96 and then add it to the
		# faces montage list
		face = cv2.resize(face, (96, 96))
		faces.append(face)

	# create a montage using 96x96 "tiles" with 5 rows and 5 columns
	montage = build_montages(faces, (96, 96), (9, 9))[0]
	
	# show the output montage
	title = "Face #{}".format(labelID)
#	title = "Unknown Faces" if labelID == -1 else title
	new_filename = 'flickr_%.3f_%d_%d_%04d_%s.jpg' % (THRESHOLD, start, end, c, title)
	cv2.imwrite(os.path.join(CLUSTER_IMAGE_DIR, new_filename), montage)
	#cv2.imshow(title, montage)
	#cv2.waitKey(0)
