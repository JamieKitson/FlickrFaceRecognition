import auth
import flickrapi
import urllib.request
import configparser
import os

PER_PAGE = 100
MAX_SIZE = 1000
DIR = 'img'

os.makedirs(DIR, exist_ok=True)

flickr = auth.get_flickr()

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
        orig = photo.get('originalformat')

        # Get photo sizes
        sizes = flickr.photos.getSizes(photo_id=photoId)
        curMax = -1
        form = 'jpg'
        url = ''
        for size in sizes.find('sizes'):
            #print(size)
            maxSide = max(int(size.get('width')), int(size.get('height')))
            if maxSide > curMax and maxSide <= MAX_SIZE and (orig == 'jpg' or size.get('label') != 'Original'):
                curMax = maxSide
                url = size.get('source')
                form = 'jpg' if size.get('label') != 'Original' else photo.get('originalformat')

        if (url == '')
            print('No URL found for ', photoId)
            continue

        fileName = os.path.join(DIR, '%s.%s' % (photoId, form))
        print(url, fileName)
        urllib.request.urlretrieve(url, fileName)

    startimage = 0
    ipage += 1


