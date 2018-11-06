# FlickrFaceRecognition

Facial recognition for Flickr

## Process

### Download, Detect and Encode Faces

The `download.py` script will:

1. authenitcate with Flickr
2. download all your images at or below MAX_SIZE
3. detect faces using DETECTION_METHOD and
4. encode faces, saving the results

The index of the image currently being processed is saved to the config.ini so you should be able to stop and restart the script at will.

There is a balance to be made with MAX_SIZE, larger images will take longer to download, take up more disk space and take more memory (possibly more than you have) and CPU process.

The DETECTION_METHOD _cnn_ or _hog_ will make a difference to speed and accuracy, _cnn_ being the slower but more accurate of the two. Personally I have found _cnn_ to be at least as quick as downloading at less than 1000px on the GPU on my Dell 9550 and a 10meg connection.

### Cluster Faces

The cluster_faces.py script will try to recognise

## Prerequisites

### Python Packages

* [flickrapi](https://github.com/sybrenstuvel/flickrapi/)
* [face-recognition](https://github.com/ageitgey/face_recognition)
* [dlib](https://github.com/davisking/dlib/) (With CUDA/GPU support where applicable.)
* [OpenCV](https://sourceforge.net/projects/opencvlibrary/)
