import cv2
import numpy as np


def nothing(x):
    pass


def generate_threshold(color, l_h, l_s, l_v, u_h, u_s, u_v, min_area, arc_factor):
    lower_red = np.array([l_h, l_s, l_v])
    upper_red = np.array([u_h, u_s, u_v])

    mask = cv2.inRange(hsv, lower_red, upper_red)

    kernel = np.ones((5, 5), np.uint8)  # black square
    mask = cv2.erode(mask, kernel)

    _, threshold = cv2.threshold(mask, 150, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours


path_to_video = '../resources/output.avi'
cap = cv2.VideoCapture(path_to_video)

while True:
    triangle_count = 0
    rectangle_count = 0
    circle_count = 0

    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    black_contours = generate_threshold("black", 0, 0, 40, 180, 98, 247, 200, 0.03)
    blue_contours = generate_threshold("blue", 106, 12, 127, 127, 76, 202, 200, 0.03)
    green_contours = generate_threshold("green", 35, 37, 107, 77, 255, 255, 200, 0.03)
    pink_contours = generate_threshold("pink", 134, 35, 60, 180, 255, 255, 200, 0.03)
    yellow_contours = generate_threshold("yellow", 0, 46, 193, 34, 255, 255, 200, 0.03)

    font = cv2.FONT_HERSHEY_COMPLEX

    # contours = black_contours + blue_contours + green_contours + pink_contours
    contours = yellow_contours + green_contours + pink_contours
    for cnt in contours:
        area = cv2.contourArea(cnt)

        if area > 250:

            approx = cv2.approxPolyDP(cnt, 0.03 * cv2.arcLength(cnt, True), True)
            cv2.drawContours(frame, [approx], 0, (0))
            print(len(approx))

            x = approx.ravel()[0]
            y = approx.ravel()[1]

            if len(approx) == 3:
                print(approx)
                cv2.putText(frame, "Triangle", (x, y), font, 0.3, (0))
                triangle_count += 1

            elif len(approx) == 4:
                print(approx)
                cv2.putText(frame, "Rectangle", (x, y), font, 0.3, (0))
                rectangle_count += 1


            elif 6 < len(approx) < 15:
                print(approx)
                cv2.putText(frame, "Circle", (x, y), font, 0.3, (0))
                circle_count += 1

    triangle_text = 'Triangles: ' + str(triangle_count)
    rectangle_text = 'Rectangles: ' + str(rectangle_count)
    circles_text = 'Circles: ' + str(circle_count)

    cv2.putText(frame, triangle_text, (100, 100), font, 0.6, (0))
    cv2.putText(frame, rectangle_text, (100, 120), font, 0.6, (0))
    cv2.putText(frame, circles_text, (100, 140), font, 0.6, (0))

    cv2.imshow('original', frame)

    # cv2.imshow("threshold", threshold)

    # cv2.imshow("Mask", mask)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()
