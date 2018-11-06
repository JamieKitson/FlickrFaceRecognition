import configparser
import os
    

class ffrsettings:

    def __init__(self):
        self.configParser = configparser.RawConfigParser()
        self.configParser.read('config.ini')

    @property
    def startimage(self):
        return self.configParser['flickr'].getint('startimage', 0)

    @startimage.setter
    def startimage(self, startimage):
        self.configParser.set('flickr', 'startimage', startimage)
        with open('config.ini', 'w') as configfile:
            self.configParser.write(configfile)

    @property
    def flickrkey(self):
        return self.configParser.get('flickr', 'key')

    @property
    def flickrsecret(self):
        return self.configParser.get('flickr', 'secret')

    @property
    def flickrsearchpagesize(self):
        return self.configParser['flickr'].getint('pagesize', 100)

    @property
    def maximagesize(self):
        return self.configParser['flickr'].getint('maximagesize', 1000)

    def getpath(self, path):
        res = self.configParser['paths'].get(path, path)
        os.makedirs(res, exist_ok=True)
        return res

    @property
    def imgdir(self):
        return self.getpath('imgs')

    @property
    def encodingsdir(self):
        return self.getpath('encodings')

    @property
    def resultsdir(self):
        return self.getpath('results')

    @property
    def detectionmethod(self):
        return self.configParser['recognition'].get('detectionmethod', 'ncc')

    @property
    def threshold(self):
        return self.configParser['recognition'].getfloat('threshold', 0.4)


