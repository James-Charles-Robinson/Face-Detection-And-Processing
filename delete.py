import cv2
import numpy as np
from PIL import Image, ImageFilter
import glob
import imutils
import random
import shutil,os

'''
Deletes photos in the face directories that are very simular or dupes
This ensures a diverse range of faces and expressions
'''

dupes = []
ims = os.listdir("faces/")
for name in ims: #for face in faces folder
    print(name)
    try:
        filename = "faces/" + name
        
        im_a = cv2.imread(filename)
        width, height, channel = im_a.shape
        ims.remove(name)

        #get image average row and total average colours
        a_avg_row = np.average(im_a, axis=0)
        a_avg_colour = np.average(a_avg_row, axis=0)

        #compares this image to all the other images
        for name2 in ims:
            try:
                filename2 = "faces/" + name2
                
                im_b = cv2.imread(filename2)
                try:
                    im_b = cv2.resize(im_b,(width,height))
                except:
                    im_b = cv2.imread(filename2)
                    
            
                b_avg_row = np.average(im_b, axis=0)
                b_avg_colour = np.average(b_avg_row, axis=0)

                row_diff = 0
                # gets the difference between each row
                for row in range(len(a_avg_row)):
                    try:
                        diff_b = a_avg_row[row][0] - b_avg_row[row][0]
                        diff_g = a_avg_row[row][1] - b_avg_row[row][1]
                        diff_r = a_avg_row[row][2] - b_avg_row[row][2]
                        if diff_b < 0:
                            diff_b *= -1
                        if diff_g < 0:
                            diff_g *= -1
                        if diff_r < 0:
                            diff_r *= -1
                        row_diff += (diff_b + diff_g + diff_r)
                    except: pass

                #gets the total difference of colours                
                diff_b = a_avg_colour[0] - b_avg_colour[0]
                diff_g = a_avg_colour[1] - b_avg_colour[1]
                diff_r = a_avg_colour[2] - b_avg_colour[2]

                if diff_b < 0:
                    diff_b *= -1
                if diff_g < 0:
                    diff_g *= -1
                if diff_r < 0:
                    diff_r *= -1

                #if the total difference is below 4 and the average row diff
                #is less than 4 aswell, move the face to dupes folder
                if diff_b + diff_g + diff_r < 4 and row_diff/width < 6:
                    print(name, name2)
                    shutil.move(filename2, "dupes/")
                    dupes.append(name2)
            except: pass
    except: pass

print("Done,", len(dupes), "dupes found")
