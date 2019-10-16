import cv2
import numpy as np
from PIL import Image, ImageFilter
import glob
import imutils
import random
import shutil
import os

'''
This program takes images and videos and outputs the face
blurred version. It also saves the faces to the faces folder
'''

# cv2 cascades
face_cascade1 = cv2.CascadeClassifier(
    "cascades/data/haarcascade_frontalface_alt2.xml")
face_cascade2 = cv2.CascadeClassifier(
    "cascades/data/haarcascade_frontalface_default.xml")
face_cascade3 = cv2.CascadeClassifier(
    "cascades/data/haarcascade_frontalface_alt.xml")


# moves files from input to done when done
def Move():
    for filename in glob.glob('input/*'):
        try:
            shutil.move(filename, "done/")
        except Exception as e:
            print (e)
            os.remove(filename)


# detects faces in an images
def GetFace(image):
    faces = []
    faces1 = face_cascade1.detectMultiScale(image,
                                            scaleFactor=1.5, minNeighbors=5)
    faces2 = face_cascade2.detectMultiScale(image,
                                            scaleFactor=1.5, minNeighbors=5)
    faces3 = face_cascade3.detectMultiScale(image,
                                            scaleFactor=1.5, minNeighbors=5)

    # get faces
    for i in range(len(faces1)):
        faces.append(faces1[i])
    for i in range(len(faces2)):
        faces.append(faces2[i])
    for i in range(len(faces3)):
        faces.append(faces3[i])
    if len(faces) > 0:
        pass
    else:
        faces = []
    return faces


# for videos continues to blur for 40 frames after the face is lost
# as long as a scene change isnt detected
def Continue(frame_i, last_index, last_faces, frame, size):

    for last_face in last_faces:
        if (frame_i - last_index < 40 and last_face != 0 and
                last_index != frame_i):

            x, y, w, h = last_face

            roi_colour = frame[y:y+h, x:x+w]

            frame = Blur(roi_colour, x, y, frame, size)

    return frame


# saves the face in the face folder
def SaveFace(i, roi):

    name = "faces/face-" + str(i) + ".png"
    print("Face Found,", name)
    cv2.imwrite(name, roi)


# sort faces largest to smallest
def SortFace(faces):
    new_faces = []
    lar_width = 0
    for face in faces:
        width = face[0] - face[1]
        if width > lar_width:
            lar_width = width
            new_faces.insert(0, face)
        else:
            new_faces.append(face)

    return new_faces


# detects if the same face has been multidetected and removes it
def Same(faces, allow):
    new_faces = []
    for i in range(len(faces)):

        same_face = False
        face = faces[i]
        if i == 0:
            new_faces.append(faces[i])
        else:

            for pre_face in new_faces:

                same_values = 0
                for cor in range(4):

                    pre_face_cor = pre_face[cor]
                    face_cor = face[cor]
                    if (pre_face_cor - face_cor > -allow and
                            pre_face_cor - face_cor < allow):

                        same_values += 1

                if same_values == 4:

                    same_face = True
            if same_face is False:

                new_faces.append(face)
    return new_faces


# blur the face in videos
def Blur(roi, x, y, frame, size):
    # blur strength depends on size of face
    w, h = size
    w = int(w * 0.1)
    h = int(h * 0.1)
    if w % 2 == 0:
        w -= 1
    if h % 2 == 0:
        h -= 1
    try:
        blur_face = cv2.GaussianBlur(roi, (w, h), 30)
        if w > 400 or h > 400:
            blur_face = cv2.blur(blur_face, (w, h), 30)
        frame[y:y+blur_face.shape[0], x:x+blur_face.shape[1]] = blur_face
    except Exception as e:
        print(e)
    return frame


# detects a scene change reliably using average face colour
def SceneChange(frame, last_colour, last_index):

    avg_row = np.average(frame, axis=0)
    avg_colour = np.average(avg_row, axis=0)

    diff_b = last_colour[0] - avg_colour[0]
    diff_g = last_colour[1] - avg_colour[1]
    diff_r = last_colour[2] - avg_colour[2]
    if diff_b < 0:
        diff_b *= -1
    if diff_g < 0:
        diff_g *= -1
    if diff_r < 0:
        diff_r *= -1

    if diff_b + diff_g + diff_r > 30:
        print("Scene Change")
        last_index = 0

    last_colour = avg_colour
    return last_colour, last_index


# saves the final video
def SaveVideo(size, fps, filename, out_img):
    out = cv2.VideoWriter(
                        (filename),
                        cv2.VideoWriter_fourcc(*"MP4V"),
                        fps,
                        size)
    for i in range(len(out_img)):
        out.write(out_img[i])
    out.release()


# saves the blurred image
def SaveImage(i, im):

    name = "output/image-" + str(i) + ".png"
    cv2.imwrite(name, im)


# the main function for videos
def Videos():

    for filename in glob.glob('input/*.mp4'):  # mp4's in input folder

        cap = cv2.VideoCapture(filename)  # video stored as cap
        size = (int(cap.get(3)), int(cap.get(4)))
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        durr = frame_count/fps
        frame_i = 0  # frame index
        last_saved_index = 0  # last index saved
        last_index = 0  # last face found
        last_colour = [0, 0, 0]
        out_img = []

        # video is max 5 mins
        if durr > 300:
            print("Video Too Long,", durr, "seconds")
            continue

        while (True):  # loop for each frame in the vid
            try:
                ret, frame = cap.read()
                grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                # frame in grey scale
            except:
                break  # when the videos over

            if frame_i % 5 == 0:
                # get faces using cv2 cascade
                faces = GetFace(grey)
                faces = SortFace(faces)
                faces = Same(faces, size[0]/10)

                # for found faces get boundaries
                if len(faces) > 0:
                    last_faces = []  # last face position
                for (x, y, w, h) in faces:
                    x -= int((size[0])/40)
                    y -= int((size[1])/40)
                    w += int((size[0])/20)
                    h += int((size[1])/20)
                    roi_colour = frame[y:y+h, x:x+w]

                    # save face every once and a while
                    if frame_i - last_saved_index > 15:

                        # SaveFace(frame_i+random.randint(0, 1000), roi_colour)
                        last_saved_index = frame_i

                    # blur face and put it back onto frame
                    frame = Blur(roi_colour, x, y, frame, size)

                    last_faces.append((x, y, w, h))
                    last_index = frame_i

                # detect scene change
                last_colour, last_index = SceneChange(
                                                    frame,
                                                    last_colour,
                                                    last_index)

            # when face is lost, keep bluring for more frames
            frame = Continue(frame_i, last_index, last_faces, frame, size)

            # cv2.imshow("frame", frame)
            # add final image to list
            out_img.append(frame)

            if cv2.waitKey(20) & 0xFF == ord("q"):
                break

            frame_i += 1
            if frame_i % 25 == 0:
                print("frame", frame_i, "/", frame_count)

        cap.release()
        filename = "output\\" + filename.split("\\")[1]
        print(filename)
        SaveVideo(size, fps, filename, out_img)

    cv2.destroyAllWindows()


# main func for photos
def Photos():

    for filename in glob.glob('input/*'):  # everythin else in input folder
        if "jpg" in filename or "png" in filename:

            print(filename)

            im = cv2.imread(filename)
            height, width, channels = im.shape
            try:
                grey = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                # frame in grey scale
            except:
                pass

            # get faces using cv2 cascade
            faces = GetFace(grey)

            # for found faces get boundaries
            for (x, y, w, h) in faces:

                roi_colour = im[y:y+h, x:x+w]

                # SaveFace(random.randint(1000, 10000), roi_colour)

                im = Blur(roi_colour, x, y, im, (height, width))
                # cv2.imshow("frame", im)
            SaveImage(random.randint(1, 10000), im)


Videos()
Photos()
Move()
