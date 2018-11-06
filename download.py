import auth
import flickrapi
import urllib.request
import ffrsettings
from os import path
import face_recognition
import pickle
import cv2
import time
from threading import Thread

settings = ffrsettings.ffrsettings()

PER_PAGE = settings.flickrsearchpagesize
MAX_SIZE = settings.maximagesize
DIR = settings.imgdir
DETECTION_METHOD = settings.detectionmethod
PICKLE_DIR = settings.encodingsdir


def retry(func, **args):
    i = 0
    while True:
        try:
            return func(**args)
        except:
            i += 1
            if i > 3:
                raise


def downloadBestSize(photoId, origIsJpg, fileName, flickr):
    #print('downloading')
    #t = time.time()
    # Get photo sizes
    sizes = retry(flickr.photos.getSizes, photo_id=photoId)
    curMax = -1
    url = ''
    for size in sizes.find('sizes'):
        #print(size)
        try:
            maxSide = max(int(size.get('width')), int(size.get('height')))
        except:
            continue
        isOrig = size.get('label', 'not') == 'Original'
        isPhoto = size.get('media', 'photo') == 'photo'
        if maxSide > curMax and maxSide <= MAX_SIZE and (origIsJpg or not isOrig):
            curMax = maxSide
            url = size.get('source')

    if url == '':
        print('No URL found for ', photoId)
        return False

    #print(url, fileName)
    urllib.request.urlretrieve(url, fileName)
    #print('Downloaded ', time.time() -t)
    return True


def encodeFaces(fileName, photoId):
    #print('encoding')
    #t = time.time()
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

    f = open(path.join(PICKLE_DIR, photoId + '.pickle'), "wb")
    f.write(pickle.dumps(d))
    f.close()
    #print('Encoded ', time.time() -t)


def main():

    flickr = auth.get_flickr()

    startimage = settings.startimage
    ipage = startimage // PER_PAGE
    startimage = startimage % PER_PAGE
    pages = ipage
    p = None

    while ipage <= int(pages):

        res = retry(
            flickr.photos.search, 
            user_id='me', 
            sort='date-posted-asc', 
            per_page=PER_PAGE, 
            page=(ipage + 1), 
            extras='original_format',
            text='IMG_20160618_091603'
            )

        xmlPhotos = res.find('photos')
        pages = xmlPhotos.get('pages')
        iphotos = xmlPhotos.get('total')
        photos = xmlPhotos.findall('photo')

        for iphoto in range(startimage, len(photos)):

            # Write image index back to ini file
            totalstartimage = iphoto + ipage * PER_PAGE
            settings.startimage = totalstartimage

            # Get photo details
            photo = photos[iphoto]
            photoId = photo.get('id')
            origIsJpg = photo.get('originalformat') == 'jpg'

            fileName = path.join(DIR, photoId + '.jpg')

            t = time.time()
            if not os.isfile(fileName):
                downloadBestSize(photoId, origIsJpg, fileName, flickr)

            if os.isfile(fileName):
                if (p != None):
                    p.join()
                #print('Downloading', time.time() - t)
                #print('starting')
                p = Thread(target=encodeFaces, args=(fileName, photoId))
                p.start()
                #print('started')
            
            #print('Downloaded ', time.time() - t)

            print(totalstartimage, "/", iphotos, time.time() - t, '\r', end="", flush=True)

        startimage = 0
        ipage += 1

if __name__ == '__main__':
    main()

