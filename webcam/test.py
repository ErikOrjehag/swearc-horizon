

import numpy as np
import cv2
import cv2.cv
import sys
import time


def threshold_img(img):
    viu, satu, hueu, vil, satl, huel = determen_hsv()

    # Blur to reduce junk. Must be an odd number.
    median = cv2.medianBlur(img, 5)

    hsv = cv2.cvtColor(median, cv2.COLOR_BGR2HSV)
    lower = np.array([huel, satl, vil])
    upper = np.array([hueu, satu, viu])

    mask = cv2.inRange(hsv, lower, upper)

    # Kernel slides through the image. A pixel will be considered
    # white only if all pixels under the kernel are white.
    kernel = np.ones((10, 10), np.uint8)

    # Remove black junk inside objects.
    closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # Remove white junk outside objects.
    opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)

    return opening


def find_circles(cnt1, res):

    acc = 2
    odia = 0
    for cnt in cnt1:
        count = 0
        old_dis = 0
        for pnt in cnt[0:(len(cnt)/4)]:
            a = tuple(pnt[0])
            b = tuple(cnt[(len(cnt)/2)+count][0])
            c = tuple(cnt[(len(cnt)/4)+count][0])
            d = tuple(cnt[(len(cnt)/2)+(len(cnt)/4)+count][0])
            cv2.line(res, a, b, (255,0,0))
            dxa = a[0]-b[0]
            dya = a[1]-b[1]
            disa = np.sqrt((dxa*dxa+dya*dya))
            dxb = c[0]-d[0]
            dyb = c[1]-d[1]
            disb = np.sqrt((dxb*dxb+dyb*dyb))
            area = cv2.contourArea(cnt)
            dia = np.sqrt(4*area/np.pi)
            leftmost = tuple(cnt[cnt[:,:,0].argmin()][0])
            rightmost = tuple(cnt[cnt[:,:,0].argmax()][0])
            topmost = tuple(cnt[cnt[:,:,1].argmin()][0])
            bottommost = tuple(cnt[cnt[:,:,1].argmax()][0])
            dxttb = topmost[0]-bottommost[0]
            dyttb = topmost[1]-bottommost[1]
            disttb = np.sqrt((dxttb*dxttb+dyttb*dyttb))
            dxltr = leftmost[0]-rightmost[0]
            dyltr = leftmost[1]-rightmost[1]
            disltr = np.sqrt((dxltr*dxltr+dyltr*dyltr))
            if  disb - acc < disa < disb + acc and dia - acc <= disa <= dia + acc and disltr - acc <= disttb <= disltr + acc:
                x,y,w,h = cv2.boundingRect(cnt)
                cv2.rectangle(res,(x,y),(x+w,y+h),[0,255,255],2)
            count = count + 1
            odia = dia


def determen_hsv():
    viu = cv2.getTrackbarPos("Vi_Upper", 'image')
    satu = cv2.getTrackbarPos("Sat_Upper", 'image')
    hueu = cv2.getTrackbarPos("Hue_Upper", 'image')
    vil = cv2.getTrackbarPos("Vi_Lower", 'image')
    satl = cv2.getTrackbarPos("Sat_Lower", 'image')
    huel = cv2.getTrackbarPos("Hue_Lower", 'image')
    return viu,satu,hueu,vil,satl,huel


def find_red_circle(frame):
    img = threshold_img(frame)
    res = cv2.bitwise_and(frame, frame, mask=img)
    contours, hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    find_circles(contours,res)
    cv2.drawContours(res, contours, -1, (0,255,0), 3)
    return res


def nothing():
    pass

if len(sys.argv) > 1 and sys.argv[1] == "--video":
    cap = cv2.VideoCapture("ticket.mp4")
else:
    cap = cv2.VideoCapture(0)

cv2.namedWindow('image', flags=cv2.WINDOW_NORMAL)

cv2.createTrackbar("Hue_Upper", 'image', 15, 255, nothing)

cv2.createTrackbar("Sat_Upper", 'image', 255, 255, nothing)

cv2.createTrackbar("Vi_Upper", 'image', 255, 255, nothing)

cv2.createTrackbar("Hue_Lower", 'image', 0, 255, nothing)

cv2.createTrackbar("Sat_Lower", 'image', 115, 255, nothing)

cv2.createTrackbar("Vi_Lower", 'image', 115, 255, nothing)


startTime = time.time()
prevTime = None

# Capture frame-by-frame
ret, frame = cap.read()

while True:

    # FPS
    nowTime = time.time()
    if prevTime:
        print("%3d fps" % (1 / (nowTime - prevTime)))
    prevTime = nowTime

    scale = 0.3

    small = cv2.resize(frame, (0, 0), fx=scale, fy=scale)

    sample = find_red_circle(small)

    cv2.imshow('original', small)
    cv2.imshow('result', sample)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
