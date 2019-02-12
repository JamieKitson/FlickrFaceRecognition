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

#THRESHOLD = settings.threshold
CLUSTER_IMAGE_DIR = settings.resultsdir
PICKLES_DIR = settings.encodingsdir
IMG_DIR = settings.imgdir

picklefile = sys.argv[1]

with open(picklefile, "rb") as f:
	tup = pickle.loads(f.read())

data = tup[0]
labels = tup[1]

#print(type(labels))
#print(labels)

counts = collections.Counter(labels)

# determine the total number of unique faces found in the dataset
labelIDs = np.unique(labels)
labelIDs = sorted(labelIDs, key=lambda x: -counts[x])

#withCounts = np.unique(labels, return_counts=True)

#print(withCounts[1])
#print(type(withCounts[1]))
#labelIDs = withCounts[0].argsort(withCounts[1].astype(np.int64))
#print(labelIDs)

numUniqueFaces = len(labelIDs)
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
	todsp = np.random.choice(idxs, size=min(81, len(idxs)),
		replace=False)

	# initialize the list of faces to include in the montage
	faces = []

	# loop over the sampled indexes
	for i in todsp:
		#print(data[i])
		# load the input image and extract the face ROI
		image = cv2.imread(path.join(IMG_DIR, data[i]["photoId"] + '.jpg'))
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
	new_filename = 'flickr_%s_%04d_%s.jpg' % (path.basename(picklefile), c, title)
	print("writing " + path.join(CLUSTER_IMAGE_DIR, new_filename))
	cv2.imwrite(path.join(CLUSTER_IMAGE_DIR, new_filename), montage)
	print("Once you have examined the image press any key. If you are happy then enter the tag. If you are unhappy don't.")
	cv2.imshow(title, montage)
	cv2.waitKey(0)
	
	tag = str(input('Tag:'))
	if tag != '':
		with open("test.txt", "a") as myfile:
			myfile.write("tag:%s\n" % tag)
			for i in idxs:
				myfile.write(data[i]["photoId"] + "\n")

		with open("html/%s.html" % tag, "a") as myfile:
			for i in idxs:
				myfile.write('<a href="https://www.flickr.com/photo.gne?id={0}"><img src="../img/{0}.jpg" style="height:150"></a>\n'.format(data[i]["photoId"]))

	cv2.destroyAllWindows()
