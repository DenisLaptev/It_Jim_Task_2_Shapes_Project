import cv2
import numpy as np
import matplotlib.pyplot as plt

'''
The idea here is to extract the moving foreground 
from the static background. 
You can also use this to compare two similar images, 
and immediately extract the differences between them.
'''

path_to_video = '../resources/output.avi'
cap = cv2.VideoCapture(path_to_video)
fgbg = cv2.createBackgroundSubtractorMOG2()

while True:
    ret, frame = cap.read()
    fgmask = fgbg.apply(frame)

    # median = cv2.medianBlur(fgmask, 5)

    cv2.imshow('original', frame)
    cv2.imshow('fg', fgmask)
    # cv2.imshow('median', median)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()
