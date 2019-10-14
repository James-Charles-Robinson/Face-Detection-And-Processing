import cv2
import numpy as np
from PIL import Image, ImageFilter
import glob
import imutils
import random
import shutil,os

'''
Collects faces from photos and videos and saves in faces folder
'''

#cv2 cascades
face_cascade1 = cv2.CascadeClassifier(
    "cascades/data/haarcascade_frontalface_alt2.xml")
face_cascade2 = cv2.CascadeClassifier(
    "cascades/data/haarcascade_frontalface_default.xml")
face_cascade3 = cv2.CascadeClassifier(
    "cascades/data/haarcascade_frontalface_alt.xml")

#moves files from input to done
def Move():
    for filename in glob.glob('input/*'):
        try:
            shutil.move(filename, "done/")
        except Exception as e:
            print (e)
            os.remove(filename)

#detects faces in an images
def GetFace(image):
    faces = []
    faces1 = face_cascade1.detectMultiScale(image,
                                        scaleFactor=1.5, minNeighbors=5)
    faces2 = face_cascade2.detectMultiScale(image,
                                        scaleFactor=1.5, minNeighbors=5)
    faces3 = face_cascade3.detectMultiScale(image,
                                        scaleFactor=1.5, minNeighbors=5)
    
    #only get one group of faces faces
    if len(faces1) > 0:
        faces = faces1
    elif len(faces2) > 0:
        faces = faces2
    elif len(faces3) > 0:
        faces = faces3
    return faces
    
#saves the face in the face folder
def SaveFace(i, roi):
    
    name = "faces/face-" + str(i) + ".png"
    cv2.imwrite(name, roi)


# the main function for videos  
def Videos():
    
    for filename in glob.glob('input/*.mp4'): #mp4's in input folder

        cap = cv2.VideoCapture(filename) #video stored as cap
        size = (int(cap.get(3)), int(cap.get(4)))
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        durr = frame_count/fps
        frame_i = 0 #frame index
        last_saved_index = 0 #last index saved
        last_index = 0 #last face found
        last_face = 0 #last face position
        last_colour = [0, 0, 0]
        out_img = []

        #video is max 10 mins
        if durr > 600:
            print("Video Too Long,", durr, "seconds")
            continue

        while (True): #loop for each frame in the vid
            try:
                ret, frame = cap.read()
                grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                #frame in grey scale
            except:
                break #when the videos over

            #only checking every 6 frames speeds it up
            if frame_i % 6 == 0:  
                #get faces using cv2 cascade
                faces = GetFace(grey)

                #for found faces get boundaries
                for (x, y, w, h) in faces:

                    roi_colour = frame[y:y+h, x:x+w]

                    #save face every once and a while
                    if frame_i - last_saved_index > 15:

                        SaveFace(frame_i+random.randint(100, 10000), roi_colour)
                        last_saved_index = frame_i

                    last_face = (x, y, w, h)
                    last_index = frame_i

    
            frame_i += 1
            if frame_i % 10 == 0:
                print(frame_i)

        cap.release()
        
    cv2.destroyAllWindows()

def Photos():

    for filename in glob.glob('input/*'): #everything else in input folder
        if "jpg" in filename or "png" in filename:

            im = cv2.imread(filename)
            try:
                grey = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) #frame in grey scale
            except:
                pass
            
            #get faces using cv2 cascade
            faces = GetFace(grey)

            #for found faces get boundaries
            for (x, y, w, h) in faces:

                roi_colour = im[y:y+h, x:x+w]

                SaveFace(random.randint(1000, 10000), roi_colour)        


Videos()
Photos()
Move()
