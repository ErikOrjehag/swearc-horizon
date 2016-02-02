

import numpy as np
import cv2
import cv2.cv

def find_ball(frame):

    height = len(frame)
    width = len(frame[0])
    size = 200
    y_steps = height // size
    x_steps = width // size
    sample = []

    print(y_steps * x_steps)

    sample = cv2.resize(frame, (0,0), fx=0.1, fy=0.1)

    for row in sample:
        for pixel in row:
            if not (pixel[0] < 100 and pixel[1] < 100 and pixel[2] > 190):
                #print("hej")
                pixel[0] = pixel[1] = pixel[2] = np.uint8(0)
    #            pass

    return sample

#def thresholdimg(img):






def find_another_ball(frame, hueu, satu, viu, huel, satl, vil):
    sample = cv2.resize(frame, (0,0), fx=1, fy=1)
    median = cv2.medianBlur(sample,5)
    hsv = cv2.cvtColor(median, cv2.COLOR_BGR2HSV)
    lower = np.array([huel,satl,vil])
    upper = np.array([hueu,satu,viu])
    mask = cv2.inRange(hsv, lower, upper)
    #ret,thresh = cv2.threshold(mask,127,255,cv2.THRESH_BINARY)

    kernel = np.ones((10,10),np.uint8)
    closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)

    res = cv2.bitwise_and(sample,sample, mask=opening)

    cnt1, hierarchy = cv2.findContours(opening,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    odia = 0
    for cnt in cnt1:
        area = cv2.contourArea(cnt)
        dia = np.sqrt(4*area/np.pi)
        leftmost = tuple(cnt[cnt[:,:,0].argmin()][0])
        rightmost = tuple(cnt[cnt[:,:,0].argmax()][0])
        topmost = tuple(cnt[cnt[:,:,1].argmin()][0])
        bottommost = tuple(cnt[cnt[:,:,1].argmax()][0])
        dxttb = topmost[0]-bottommost[0]
        dyttb = topmost[1]-bottommost[1]
        disttb = np.sqrt((dxttb*dxttb+dyttb*dyttb))
        dxltr = topmost[0]-bottommost[0]
        dyltr = topmost[1]-bottommost[1]
        disltr = np.sqrt((dxltr*dxltr+dyltr*dyltr))
        cv2.circle(res,leftmost,5,(255,0,255))
        cv2.circle(res,topmost,5,(255,0,255))
        cv2.circle(res,bottommost,5,(255,0,255))
        cv2.circle(res,rightmost,5,(255,0,255))
        if dia-1 <= disttb <= dia+1 and disltr-1 <= disttb <= disltr+1:
            x,y,w,h = cv2.boundingRect(cnt)
            cv2.rectangle(res,(x,y),(x+w,y+h),[0,255,255],2)
            #print "red :", x,y,w,h
        odia = dia

    cv2.drawContours(res, cnt1, -1, (0,255,0), 3)


    """
    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(gray,cv2.cv.CV_HOUGH_GRADIENT,1,10)
    print circles
    if np.all(circles):
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            # draw the outer circle
            cv2.circle(gray,(i[0],i[1]),i[2],(0,255,0),2)
            # draw the center of the circle
            cv2.circle(gray,(i[0],i[1]),2,(0,0,255),3)
    """

    """
    mov = cv2.moments(opening)
    dArea = mov["m00"]
    if dArea > 1000:
        y = mov["m01"]/dArea
        x = mov["m10"]/dArea
        cv2.circle(res,(int(x),int(y)), 2, (0,0,255))
        print x
    """


    return res

def scale(frame, factor):
    big = []
    for y in range(len(frame)):
        for i in range(factor):
            big.append([])
            for x in range(len(frame[y])):
                for j in range(factor):
                    big[y * factor + i].append(frame[y][x])
    return mask

def nothing():
    pass
cap = cv2.VideoCapture(1)

cv2.namedWindow('image')

cv2.createTrackbar("Hue_Upper", 'image', 15, 255, nothing)

cv2.createTrackbar("Sat_Upper", 'image', 255, 255, nothing)

cv2.createTrackbar("Vi_Upper", 'image', 255, 255, nothing)

cv2.createTrackbar("Hue_Lower", 'image', 0, 255, nothing)

cv2.createTrackbar("Sat_Lower", 'image', 115, 255, nothing)

cv2.createTrackbar("Vi_Lower", 'image', 115, 255, nothing)
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    viu = cv2.getTrackbarPos("Vi_Upper", 'image')
    satu = cv2.getTrackbarPos("Sat_Upper", 'image')
    hueu = cv2.getTrackbarPos("Hue_Upper", 'image')
    vil = cv2.getTrackbarPos("Vi_Lower", 'image')
    satl = cv2.getTrackbarPos("Sat_Lower", 'image')
    huel = cv2.getTrackbarPos("Hue_Lower", 'image')



    sample = find_another_ball(frame, hueu, satu, viu, huel, satl, vil)

    cv2.imshow('frame1', frame)
    cv2.imshow('frame2', sample)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()




