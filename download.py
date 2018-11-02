import auth
import flickrapi
import urllib.request
import configparser
import os

#from imutils import paths
import face_recognition
#import argparse
import pickle
import cv2


PER_PAGE = 100
MAX_SIZE = 1000
DIR = 'img'
DETECTION_METHOD = 'ncc'


def encodeFaces(fileName, photoId)
    image = cv2.imread(fileName)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # detect the (x, y)-coordinates of the bounding boxes
    # corresponding to each face in the input image
    boxes = face_recognition.face_locations(rgb, model=DETECTION_METHOD)

    # compute the facial embedding for the face
    encodings = face_recognition.face_encodings(rgb, boxes)

    # build a dictionary of the image path, bounding box location,
    # and facial encodings for the current image
    d = [{"photoId": photoId, "loc": box, "encoding": enc}
        for (box, enc) in zip(boxes, encodings)]
    #data.extend(d)

    f = open(os.path.join('pickles', photoId + '.pickle'), "wb")
    f.write(pickle.dumps(d))
    f.close()


flickr = auth.get_flickr()

os.makedirs(DIR, exist_ok=True)

configParser = configparser.RawConfigParser()
configParser.read('config.ini')

startimage = configParser['flickr'].getint('startimage', 0)
ipage = startimage // PER_PAGE
startimage = startimage % PER_PAGE
pages = ipage

while ipage <= pages:

    res = flickr.photos.search(user_id='me', sort='date-posted-asc', per_page=PER_PAGE, page=(ipage + 1), extras='original_format')

    xmlPhotos = res.find('photos')
    pages = xmlPhotos.get('pages')
    iphotos = xmlPhotos.get('total')
    photos = xmlPhotos.findall('photo')

    for iphoto in range(startimage, len(photos)):

        # Write image index back to ini file
        totalstartimage = iphoto + ipage * PER_PAGE
        configParser.set('flickr', 'startimage', totalstartimage)
        with open('config.ini', 'w') as configfile:    # save
            configParser.write(configfile)
        print(totalstartimage, "/", iphotos)
        #, '\r', end="", flush=True)

        # Get photo details
        photo = photos[iphoto]
        photoId = photo.get('id')
        origIsJpg = photo.get('originalformat') == 'jpg'

        # Get photo sizes
        sizes = flickr.photos.getSizes(photo_id=photoId)
        curMax = -1
        url = ''
        for size in sizes.find('sizes'):
            #print(size)
            try:
                maxSide = max(int(size.get('width')), int(size.get('height')))
            except:
                continue
            isOrig = size.get('label') == 'Original'
            if maxSide > curMax and maxSide <= MAX_SIZE and (origIsJpg or not isOrig):
                curMax = maxSide
                url = size.get('source')

        if url == '':
            print('No URL found for ', photoId)
            continue

        fileName = os.path.join(DIR, photoId + '.jpg')
        print(url, fileName)
        urllib.request.urlretrieve(url, fileName)

        image = cv2.imread(fileName)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # detect the (x, y)-coordinates of the bounding boxes
        # corresponding to each face in the input image
        boxes = face_recognition.face_locations(rgb, model=DETECTION_METHOD)

        # compute the facial embedding for the face
        encodings = face_recognition.face_encodings(rgb, boxes)

        # build a dictionary of the image path, bounding box location,
        # and facial encodings for the current image
        d = [{"photoId": photoId, "loc": box, "encoding": enc}
            for (box, enc) in zip(boxes, encodings)]
        #data.extend(d)

        f = open(os.path.join('pickles', photoId + '.pickle'), "wb")
        f.write(pickle.dumps(d))
        f.close()

    startimage = 0
    ipage += 1


