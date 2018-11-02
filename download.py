import auth
import flickrapi
import urllib.request
import os.path
import configparser

PER_PAGE = 100
SIZE = 'url_z'
MAX_SIZE = 1000

flickr = auth.get_flickr()

configParser = configparser.RawConfigParser()
configParser.read('config.ini')
#flickrconfig = configParser['flickr'] 

#ipage = configParser['flickr'].getint('page', '1')
startimage = configParser['flickr'].getint('startimage', 0)
ipage = startimage // PER_PAGE
startimage = startimage % PER_PAGE
pages = ipage

#print(ipage)
#print(startimage)
#print(type(pages))

#for ipage in range(ipage, pages):
while ipage <= pages:
    res = flickr.photos.search(
            #tag_mode='all',
            #tags='sybren,365,threesixtyfive',
            #min_taken_date='2008-08-20',
            #max_taken_date='2008-08-30'
            user_id='me',
            sort='date-posted-asc',
            per_page=PER_PAGE,
            extras=SIZE,
            page=(ipage + 1),
            )
    pages = res.find('photos').get('pages')
    iphotos = res.find('photos').get('total')
    photos = res.find('photos').findall('photo')
    # print(pages)

#for child in photos.find('photos').iter('photo'):
#    print(child.tag, child.attrib)

    for iphoto in range(startimage, len(photos)):
        totalstartimage = iphoto + ipage * PER_PAGE
        configParser.set('flickr', 'startimage', totalstartimage)
        with open('config.ini', 'w') as configfile:    # save
            configParser.write(configfile)
        print(totalstartimage, "/", iphotos, '\r', end="", flush=True)
        photo = photos[iphoto]
        photoId = photo.get('id')
        sizes = flickr.photos.getSizes(photo_id=photoId)
        curMax = -1
        for size in sizes.find('sizes'):
            #print(size)
            maxSide = max(int(size.get('width')), int(size.get('height')))
            if maxSide > curMax and maxSide <= MAX_SIZE:
                curMax = maxSide
                url = size.get('source')
            #print(maxSide, curMax)
        #url = photo.get(SIZE)
        fileName = r'img/%s.jpg' % photoId
        print(url, fileName)
        #if not os.path.isfile(fileName):
        urllib.request.urlretrieve(url, fileName)
    startimage = 0
    ipage += 1


