import os
from math import ceil

import cv2
import numpy as np

PERCENTAGE_OF_SEGMENT = 0.001


def video_to_frames(filename):
    vidcap = cv2.VideoCapture(filename)
    #success, image = vidcap.read()
    count = 0
    success = True
    images = []
    while success:
        success, image = vidcap.read()
        #print('Read a new frame: ', success)
        if success:
            images.append(image)
            count += 1
    return count, images


def make_strip_photo(column, filename):
    count, images = video_to_frames(filename)
    y, x, c = images[0].shape

    #s_height, s_width = y, ceil(x*PERCENTAGE_OF_SEGMENT)
    s_height, s_width = y, x//count
    new_image = np.zeros((s_height, s_width * count, 3), np.uint8)
    for i in range(0, count*s_width, s_width):
        new_image[0:s_height, i:i+s_width] = images[i//s_width][0:y, column:column+s_width]
    return  s_width, new_image

    #cv2.imshow('image', new_image)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

def make_strip_video(filename, output_name):
    segment_w, frame = make_strip_photo(0,filename)
    height, width, channels = frame.shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Be sure to use lower case
    out = cv2.VideoWriter(output_name, fourcc, 20.0, (width, height))
    i = 0
    while i<width-segment_w:
        tmp, frm = make_strip_photo(i,filename)
        out.write(frm)
        i+=segment_w
        print(i,"of",width-segment_w)
    # Release everything if job is finished
    out.release()


make_strip_video("normal_d.mp4","stripped.mp4")
#blank_image = np.zeros((height,width,3), np.uint8)