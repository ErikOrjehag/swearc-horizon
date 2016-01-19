
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

    #for row in sample:
    #    for pixel in row:
    #        if not (pixel[0] < 100 and pixel[1] < 100 and pixel[2] > 200):
                #print("hej")
                #pixel[0] = pixel[1] = pixel[2] = np.uint8(0)
    #            pass

    return sample

    for y in range(0, y_steps):
        sample.append([])
        for x in range(0, x_steps):

            sample_x = size / 2 + y * size
            sample_y = size / 2 + x * size

            bgr = frame[sample_x][sample_y]
            color = [bgr[0], bgr[1], bgr[2]]

            if not (color[0] < 100 and color[1] < 100 and color[2] > 200):
                color[0] = color[1] = color[2] = np.uint8(0)
            else:
                color[0] = color[1] = color[2] = np.uint8(200)

            sample[y].append(color)

    return sample


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

    sample = find_ball(frame)

    cv2.imshow('frame1', frame)
    cv2.imshow('frame2', np.array(sample))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()


