# Face-Detection-And-Processing
Three python scripts that detect faces in videos and photos, can save those faces or can blur them out and save a final image.
# How To Use
1. Download the dependancies
2. Put your input images or videos in the input folder
3. If you just want the saved faces then run the collect.py file or if you want the faces in images/videos to be blurred then run the blur.py program
4. If you want to delete very simular faces from your faces folder run the delete.py file, this deletes faces that are almost the same

# Examples

## Blur.py
### Input
![](https://github.com/James-Charles-Robinson/Face-Detection-And-Processing/blob/master/example/input/1%20-%20OwPDkI8.jpg?raw=true)
### Output
![](https://github.com/James-Charles-Robinson/Face-Detection-And-Processing/blob/master/example/output/blur/image-5322.png?raw=true)

## Collect.py
### Input
![](https://github.com/James-Charles-Robinson/Face-Detection-And-Processing/blob/master/example/input/18%20-%20jmhXqXq.jpg?raw=true)
### Output
![](https://github.com/James-Charles-Robinson/Face-Detection-And-Processing/blob/master/example/output/faces/face-1769.png?raw=true)
![](https://github.com/James-Charles-Robinson/Face-Detection-And-Processing/blob/master/example/output/faces/face-7372.png?raw=true)

To See more imputs and outputs head to the examples folder

# Limitations
1. Depending on the input photos, about 10% of outputed faces and blurred regions are false positives.
2. Sometimes the blurred region is doubled up, this is because of multidetection. I have eliminated most but not all of this.
3. Faces are not detected if they are slightly rotated in any axis, only front facing portraits can be used reliably.
4. Blurring in the videos is quite jagged/stuttery, i would like it to be smoother.

# What I Learnt
1. How to use cv2 cascades to detect objects (faces) in an image
2. How to save images using cv2
3. How roi's work in cv2
4. How to quickly get average colours in an image using cv2
5. How blur an roi using cv2's GaussianBlur function
6. How to paste that roi onto another image to get a final result
