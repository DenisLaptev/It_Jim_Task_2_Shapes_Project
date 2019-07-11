import cv2
import numpy as np


def nothing(x):
    pass


path_to_video = '../../resources/output.avi'
cap = cv2.VideoCapture(path_to_video)

path_to_picture = '../../resources/image.png'
img1 = cv2.imread(path_to_picture)

cv2.namedWindow("Trackbars")
cv2.createTrackbar("L-H", "Trackbars", 35, 180, nothing)
cv2.createTrackbar("L-S", "Trackbars", 37, 255, nothing)
cv2.createTrackbar("L-V", "Trackbars", 107, 255, nothing)
cv2.createTrackbar("U-H", "Trackbars", 77, 180, nothing)
cv2.createTrackbar("U-S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U-V", "Trackbars", 255, 255, nothing)

while True:
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


    img1_hsv = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)

    l_h = cv2.getTrackbarPos("L-H", "Trackbars")
    l_s = cv2.getTrackbarPos("L-S", "Trackbars")
    l_v = cv2.getTrackbarPos("L-V", "Trackbars")
    u_h = cv2.getTrackbarPos("U-H", "Trackbars")
    u_s = cv2.getTrackbarPos("U-S", "Trackbars")
    u_v = cv2.getTrackbarPos("U-V", "Trackbars")

    lower_color = np.array([l_h, l_s, l_v])
    upper_color = np.array([u_h, u_s, u_v])

    mask = cv2.inRange(hsv, lower_color, upper_color)
    img1_mask = cv2.inRange(img1_hsv, lower_color, upper_color)

    kernel = np.ones((5, 5), np.uint8)  # black square
    mask = cv2.erode(mask, kernel)
    img1_mask = cv2.erode(img1_mask, kernel)

    _, threshold = cv2.threshold(mask, 150, 255, cv2.THRESH_BINARY)
    _, img1_threshold = cv2.threshold(img1_mask, 150, 255, cv2.THRESH_BINARY)

    cv2.imshow('original', frame)
    cv2.imshow("threshold", threshold)

    cv2.imshow('img1_original', img1)
    cv2.imshow("img1_threshold", img1_threshold)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()
