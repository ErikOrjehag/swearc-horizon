
import numpy as np
import cv2

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


def find_another_ball(frame, hueu, satu, viu, huel, satl, vil):
    sample = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)

    hsv = cv2.cvtColor(sample, cv2.COLOR_BGR2HSV)
    lower = np.array([huel,satl,vil])
    upper = np.array([hueu,satu,viu])
    #lower = np.array([0,74,92])
    #upper = np.array([10,255,255])
    mask = cv2.inRange(hsv, lower, upper)
    res = cv2.bitwise_and(sample,sample, mask=mask)
    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(gray,127,255,0)
    contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(res, contours, -1, (0,255,0), 3)
    #print (contours)
    return res

def scale(frame, factor):
    big = []
    for y in range(len(frame)):
        for i in range(factor):
            big.append([])
            for x in range(len(frame[y])):
                for j in range(factor):
                    big[y * factor + i].append(frame[y][x])
    return big

def nothing():
    pass
cap = cv2.VideoCapture("ball_video.mp4")

cv2.namedWindow('image')

cv2.createTrackbar("Hue_Upper", 'image', 2, 255, nothing)

cv2.createTrackbar("Sat_Upper", 'image', 255, 255, nothing)

cv2.createTrackbar("Vi_Upper", 'image', 255, 255, nothing)

cv2.createTrackbar("Hue_Lower", 'image', 0, 255, nothing)

cv2.createTrackbar("Sat_Lower", 'image', 119, 255, nothing)

cv2.createTrackbar("Vi_Lower", 'image', 127, 255, nothing)
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
    cv2.imshow('frame2', np.array(sample))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()


