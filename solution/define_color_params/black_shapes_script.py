import cv2
import numpy as np


path_to_video = '../../resources/output.avi'
cap = cv2.VideoCapture(path_to_video)

path_to_picture = '../../resources/image.png'
img1 = cv2.imread(path_to_picture)



while True:
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    _, threshold = cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY)


    kernel = np.ones((5, 5), np.uint8)  # black square
    mask = cv2.erode(threshold, kernel)

    threshold_inv = cv2.bitwise_not(mask)

    kernel = np.ones((5, 5), np.uint8)  # black square

    open_frame = cv2.morphologyEx(threshold_inv, cv2.MORPH_OPEN, kernel)

    kernel = np.ones((5, 5), np.uint8)  # black square

    result_frame= cv2.erode(open_frame, kernel)


    cv2.imshow("gray", gray)
    #cv2.imshow("threshold", threshold)
    cv2.imshow("threshold_inv", threshold_inv)
    #cv2.imshow("mask", mask)
    cv2.imshow("open_frame", open_frame)
    cv2.imshow("result_frame", result_frame)





    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()
