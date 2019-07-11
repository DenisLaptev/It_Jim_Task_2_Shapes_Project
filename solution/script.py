import cv2
import numpy as np

font = cv2.FONT_HERSHEY_COMPLEX

path_to_video = '../resources/output.avi'
cap = cv2.VideoCapture(path_to_video)


def nothing(x):
    pass


def generate_threshold(color, l_h, l_s, l_v, u_h, u_s, u_v):
    if color == 'black':
        # convert to gray
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # thresholding
        _, threshold = cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY)

        # erosion
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.erode(threshold, kernel)

        # make inverse
        threshold_inv = cv2.bitwise_not(mask)

        # opening
        kernel = np.ones((5, 5), np.uint8)  # black square
        open_frame = cv2.morphologyEx(threshold_inv, cv2.MORPH_OPEN, kernel)

        # erosion
        kernel = np.ones((5, 5), np.uint8)  # black square
        result_frame = cv2.erode(open_frame, kernel)

        # thresholding
        _, threshold = cv2.threshold(result_frame, 150, 255, cv2.THRESH_BINARY)

    else:

        # convert to hsv
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # filtering
        lower_red = np.array([l_h, l_s, l_v])
        upper_red = np.array([u_h, u_s, u_v])
        mask = cv2.inRange(hsv, lower_red, upper_red)

        # erosion
        kernel = np.ones((5, 5), np.uint8)  # black square
        mask = cv2.erode(mask, kernel)

        # thresholding
        _, threshold = cv2.threshold(mask, 150, 255, cv2.THRESH_BINARY)

    # make contours
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours


while True:
    triangle_count = 0
    rectangle_count = 0
    circle_count = 0

    _, frame = cap.read()

    black_contours = generate_threshold("black", 0, 0, 40, 180, 98, 247)
    blue_contours = generate_threshold("blue", 106, 12, 127, 127, 76, 202)
    green_contours = generate_threshold("green", 35, 37, 107, 77, 255, 255)
    pink_contours = generate_threshold("pink", 134, 35, 60, 180, 255, 255)
    light_yellow_contours = generate_threshold("light_yellow", 0, 46, 193, 34, 255, 255)
    yellow_contours = generate_threshold("yellow", 24, 44, 142, 89, 76, 255)

    contours = black_contours + green_contours + pink_contours + light_yellow_contours
    # contours = yellow_contours + green_contours + pink_contours

    for cnt in contours:
        area = cv2.contourArea(cnt)

        if area > 450 and area < 25000:

            # approximation of contour by polygon
            approx = cv2.approxPolyDP(cnt, 0.03 * cv2.arcLength(cnt, True), True)
            cv2.drawContours(frame, [approx], 0, (0, 0, 255), 5)

            # alternative to approx
            # hull = cv2.convexHull(cnt)
            # cv2.drawContours(frame, [hull], 0, (0,0,255),5)

            # coordinates of the beginning of polygon for text-label
            x = approx.ravel()[0]
            y = approx.ravel()[1]

            if len(approx) == 3:
                cv2.putText(frame, "Triangle", (x, y), font, 0.5, (255, 0, 0))
                triangle_count += 1

            elif len(approx) == 4:
                cv2.putText(frame, "Rectangle", (x, y), font, 0.5, (255, 0, 0))
                rectangle_count += 1


            elif 6 < len(approx) < 15:
                cv2.putText(frame, "Circle", (x, y), font, 0.5, (255, 0, 0))
                circle_count += 1

    # str variables for (cont of polygons)
    triangle_text = 'Triangles: ' + str(triangle_count)
    rectangle_text = 'Rectangles: ' + str(rectangle_count)
    circles_text = 'Circles: ' + str(circle_count)

    # print info (cont of polygons) at the frame
    cv2.putText(frame, triangle_text, (100, 100), font, 0.6, (0))
    cv2.putText(frame, rectangle_text, (100, 120), font, 0.6, (0))
    cv2.putText(frame, circles_text, (100, 140), font, 0.6, (0))

    cv2.imshow('original', frame)

    # if 'Esc' (k==27) is pressed then break
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
