
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


def find_another_ball(frame):

    sample = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)

    hsv = cv2.cvtColor(sample, cv2.COLOR_BGR2HSV)
    lower = np.array([0,50,50])
    upper = np.array([10,255,255])
    #lower = np.array([50,50,250])
    #upper = np.array([0,0,150])
    mask = cv2.inRange(hsv, lower, upper)
    res = cv2.bitwise_and(sample,sample, mask=mask)

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


cap = cv2.VideoCapture("ball_video.mp4")

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    sample = find_another_ball(frame)

    cv2.imshow('frame1', frame)
    cv2.imshow('frame2', np.array(sample))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()


