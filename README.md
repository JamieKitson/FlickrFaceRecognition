# FlickrFaceRecognition

Facial recognition for Flickr

## Process

### 1. Download, Detect and Encode Faces

The `download.py` script will:

1. authenticate with Flickr
2. download all your images at or below MAX_SIZE
3. detect faces using DETECTION_METHOD and
4. encode faces, saving the results

The index of the image currently being processed is saved to the config.ini so you should be able to stop and restart the script at will.

There is a balance to be had with **MAX_SIZE**, larger images will take longer to download, take up more disk space and take more memory (possibly more than you have) and longer to process.

The **DETECTION_METHOD** _cnn_ or _hog_ will make a difference to the speed and accuracy of detection, _cnn_ being the slower but more accurate of the two. Personally I have found _cnn_ to be at least as quick at detecting faces as downloading at less than 1000px on a 2GB NVIDIA GeForce GTX 960M and a 10meg connection. ie, the _cnn_ detection process, run in paralell to downloading, does not add to the total running time.

### 2. Cluster Faces

The `cluster_faces.py` script will try to group similar faces together and prompt for a tag (ie, the name to the face) to save for writing back to Flickr.

**THRESHOLD** decides how similar faces have to be to be clustered and should be between 0 and 1. A lower number is stricter and leads to fewer false positives, but more and smaller groups, eg, a person might be put into different groups depending on whether they're wearing glasses or not. 

As far as I know dlib is not racist or sexist, but seems (from experience) to have been trained with [mostly][1] [white][2] men, ie, it is more accurate with white men than non-white women. In practice this means that if there are non-white/women in your dataset then you will need to set the threshold lower for more accurate results. I find 0.45 - 0.5 ok for white men but even as low as 0.4 dlib will confuse certain female Chinese/Malay friends of mine.

Having said all that, I find it better to run clustering several times, starting with a high figure of 0.5 - 0.6 and only name clusters that are sufficiently accurate. Each time you run the clustering lower the threshold by about 0.05 and name faces that you haven't named each time.

[1]: https://github.com/ageitgey/face_recognition/wiki/Face-Recognition-Accuracy-Problems#question-face-recognition-works-well-with-european-individuals-but-overall-accuracy-is-lower-with-asian-individuals
[2]: https://github.com/davisking/dlib/issues/1407

### 3. Write Tags to Flickr

The `tag_photos.py` script will read the file saved by the `cluster_faces.py` script in the previous step and write the tags back to Flickr.

## Prerequisites

### Python Packages

* [flickrapi](https://github.com/sybrenstuvel/flickrapi/)
* [face-recognition](https://github.com/ageitgey/face_recognition)
* [dlib](https://github.com/davisking/dlib/) (With CUDA/GPU support where applicable.)
* [OpenCV](https://sourceforge.net/projects/opencvlibrary/)

## Further Reading

I started at [Face clustering with Python][3]. Note that this uses `sklearn.DBSCAN` to cluster instead of `dlib.chinese_whispers`. I found the latter superior, but I didn't spend much time investigating the former which is apparently better with smaller datasets.

[3]: https://www.pyimagesearch.com/2018/07/09/face-clustering-with-python/
