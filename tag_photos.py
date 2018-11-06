import auth
import flickrapi
import time

flickr = auth.get_flickr()


with open('test.txt','r') as myfile:
    for line in myfile:
        i = 0
        t = time.time()
        if line.startswith('tag:'):
            tag = line[len('tag:'):]
        else:
            flickr.photos.addTags(photo_id=line, tags=tag)
            i += 1
        print(i, tag, time.time() - t)
#, '\r', end="", flush=True)
