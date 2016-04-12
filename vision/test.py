import numpy
import cv2
#from matplotlib import pyplot as plt



def show_camera():
    cap = cv2.VideoCapture(1)
    print(cap)

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            continue

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

        # Display the resulting frame
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()

def test_func():
    img = cv2.imread("index.jpeg", 1)
    cv2.imshow("test", img)
    while True:
        k = cv2.waitKey(1000) & 0xFF
        for row in range(len(img)):
            for pixel in range(row):
                count = 0
                for i in range(3):
                    if abs(img.item(row, pixel, i) - 255) <= 20:
                        count += 1
                if not count == 3:
                    pass
                    #print(img[row, pixel])
        print(k)
        if k > -1:
            break
    cv2.destroyAllWindows()


def show():
    img = cv2.imread("index.jpeg", 1)
    cv2.imshow('image',img)
    k = cv2.waitKey(0) & 0xFF
    if k == 27:
        cv2.destroyAllWindows()
    else:
        cv2.destroyAllWindows()


def corner_detect_harris():
    cap = cv2.VideoCapture(1)
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        #img = cv2.imread('traindoor.jpg')
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        gray = numpy.float32(gray)
        dst = cv2.cornerHarris(gray, 5, 25, 0.05)
        #print(dst)
        dst = cv2.dilate(dst, None)
        #print(dst)

        frame[dst>0.01*dst.max()] = [0, 0, 255]

        corners = []
        for row in range(len(frame)):
            for pixel in range(len(frame[row])):
                if frame.item(row, pixel, 0) == 0 and \
                   frame.item(row, pixel, 1) == 0 and \
                   frame.item(row, pixel, 2) == 255:
                    corners.append((row, pixel))
        #print(corners)
        corner.sort()
        print(sort)

        cv2.imshow('dst', frame)
        if cv2.waitKey(1) & 0xff == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


def corner_detect_subpixel():
    """
    Not working properly beacuse cv2 2.4.8 dosen't
    include cv2.connectedComponentsWithStats()

    """
    img = cv2.imread('chessboard.jpg')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gray = numpy.float32(gray)
    dst = cv2.cornerHarris(gray,2, 3, 0, 0.4)
    dst = cv2.dilate(dst, None)
    ret, dst = cv2.threshold(dst, 0.01*dst.max(), 255, 0)
    dst = numpy.uint8(dst)

    ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
    corners = cv2.cornerSubPix(gray, numpy.float32(centeroids), (5, 5),
                               (-1, -1), criteria)
    res = numpy.hstack((centeroids, corners))
    res = numpy.int0(res)
    img[res[:, 1], res[:, 0]] = [0, 0, 255]
    img[res[:, 3], res[:, 2]] = [0, 255, 0]

    cv2.imwrite('subpixel5', img)


def corner_detect_gftt():
    """
    Uses cv2.goodFeaturesToTrack() to find corners
    """
    img = cv2.imread('chessboard.jpg')
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    corners = cv2.goodFeaturesToTrack(gray, 1000, 0.001, 0.1, 10)
    # 25 is the number of corners that shall be found
    # 0 is the quality level, can be between 0-1
    # 0.1 and 10 is the minimum euclidean distance between corners
    corners = numpy.int0(corners)

    for i in corners:
        x,y = i.ravel()
        cv2.circle(img, (x,y), 3, 255, -1)

    cv2.imshow('gftt', img)
    if cv2.waitKey(0) & 0xff == 27:
        cv2.destroyAllWindows()


def corner_detect_sift():
    """
    cv2.SIFT() is not in the standard cv2, must download
    source file and compile it
    """
    img = cv2.imread('chessboard.jpg')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    sift = cv2.SIFT()
    kp = sift.detect(gray, None)

    img = cv2.drawKeypoints(gray, kp)

    cv2.imwrite('sift_keypoints.jpg', img)


def background_subtraction_mog():
    cap = cv2.VideoCapture()

    fgbg = cv2.BackgroundSubtractorMOG(10, 10, 1, 10)

    while True:
        ret, frame = cap.read()

        fgmask = fgbg.apply(frame)

        cv2.imshow('frame', fgmask)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


def detect_circle():
    """
    Think needs a newer version of cv2
    """
    img = cv2.imread('/home/zacno594/liu/robot_labbet/blidbehandling/index.jpeg')
    print(img)
    cv2.imshow('test', img)
    img = cv2.medianBlur(img, 5)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 20,
                               param1=50, param2=30, minRadius=0,
                               maxRadius=100000)

    circles = numpy.uint16(numpy.around(circles))
    for i in circles[0, :]:
        # draw the outer circle
        cv2.circle(cimg, (i[0], i[1], i[2], (0, 255, 0), 2))
        # draw the center circle
        cv2.circle(cimg, (i[0], i[1], i[2], (0, 0, 255), 3))

        cv2.imshow('detected circles', cimg)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def meanshift():
    cap = cv2.VideoCapture(1)

    ret, frame = cap.read()


    r, h, c, w = 250, 90, 400, 125
    track_window = (c, r, w, h)

    roi = frame[r:r+h, c:c+w]
    hsv_roi = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_roi, numpy.array((0., 60., 32.)),
                        numpy.array((180., 255., 255.)))
    roi_hist = cv2.calcHist([hsv_roi], [0], mask, [180], [0, 180])
    cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

    term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

    while True:
        ret, frame = cap.read()

        if ret:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)

            ret, track_window = cv2.meanShift(dst, track_window, term_crit)

            x, y, w, h = track_window
            #img2 = cv2.rectangle(frame, (x, y), (x+w, y+h), 255, 2)
            cv2.rectangle(frame, (x, y), (x+w, y+h), 255, 2)
            k = cv2.waitKey(60) & 0xff
            if k == 27:
                break
            else:
                cv2.imwrite(chr(k) + ".jpg", frame)
        else:
            break

    cv2.destroyAllWindows()
    cap.release()


def disparity_map():

    cap_l = cv2.VideoCapture(1)
    cap_r = cv2.VideoCapture(2)

    #imgL = cv2.imread('traindoor.jpg',0)
    #imgR = cv2.imread('traindoor.jpg',0)


    while True:
        ret_l, frame_l = cap_l.read()
        ret_r, frame_r = cap_r.read()

        gray_l = cv2.cvtColor(frame_l, cv2.COLOR_BGR2GRAY)
        gray_r = cv2.cvtColor(frame_r, cv2.COLOR_BGR2GRAY)

        #stereo = cv2.StereoBM(numDisparities=16, blockSize=15)
        stereo = cv2.StereoBM(cv2.STEREO_BM_BASIC_PRESET,ndisparities=16,
                              SADWindowSize=15)
        print(stereo)
        disparity = stereo.compute(gray_l, gray_r)

        cv2.imshow('3d', disparity)
        cv2.imshow('left', gray_l)
        cv2.imshow('right', gray_r)

        keyboard = cv2.waitKey(1)
        if keyboard & 0xFF == ord('q'):
            break
    cap_r.release()
    cap_l.release()
    cv2.destroyAllWindows()




def haar_cascade():

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    body_cascade = cv2.CascadeClassifier('haarcascade_upperbody.xml')

    cap = cv2.VideoCapture(1)

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        bodys = body_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in bodys:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            gray[y:y+h, x:x+w]
            frame[y:y+h, x:x+w]
            faces = face_cascade.detectMultiScale(gray)
            for (ex,ey,ew,eh) in faces:
                cv2.rectangle(frame,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        cv2.imshow('frame', frame)

        keyboard = cv2.waitKey(1)
        if keyboard & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

