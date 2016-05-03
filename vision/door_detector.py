import numpy as np
import cv2
#from matplotlib import pyplot as plt

corner = False

#img = cv2.imread('OpenCV_Chessboard.png',0)
img = cv2.imread("traindoor.jpg", 0)
if img is not None and corner:
    # Initiate STAR detector
    orb = cv2.ORB()

    # find the keypoints with ORB
    kp = orb.detect(img,None)

    # compute the descriptors with ORB
    kp, des = orb.compute(img, kp)

    combined = 0.0
    for e in kp:
        combined += e.response

    groups = []
    for i in range(len(kp)):
        groups.append((kp[i].pt,[]))
        for j in range(len(kp)-i):
            if not kp[i].pt == kp[i+j].pt:
                abs_x = abs(kp[i].pt[0] - kp[i+j].pt[0])
                abs_y = abs(kp[i].pt[1] - kp[i+j].pt[1])
                #print(str(abs_x) + " | " + str(kp[i].pt[0]) + ":" +
                #      str(kp[i+j].pt[0]) + " y " +
                #      str(abs_y) + " | " + str(kp[i].pt[1]) + ":" +
                #      str(kp[i+j].pt[1]))
                if abs_x < 10 and \
                   abs_y < 10:
                    groups[i][1].append(kp[i+j].pt)



    print(len(kp))
    medel = combined / len(kp)
    print(medel)
    reduced = []
    print(groups)
    #for e in kp:
    #    if e.response > medel:
    #        reduced.append(e)

    #reduced = sorted(kp, key=lambda e: e.response)

    #print(len(reduced))


    # draw only keypoints location,not size and orientation
    img2 = cv2.drawKeypoints(img,kp,color=(0,255,0), flags=0)
    cv2.namedWindow("Corner")
    cv2.imshow("Corner",img2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    #plt.imshow(img2),plt.show()
elif img is not None and not corner:

    #gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gray = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    edges = cv2.Canny(gray,50,150,apertureSize = 3)

    lines = cv2.HoughLines(edges,1,np.pi/180,200)
    start_coord = []
    end_coord = []
    for rho,theta in lines[0]:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))
        start_coord.append((x1,y1))
        end_coord.append((x2,y2))

    for i in range(len(start_coord)):
        removed = 0
        for j in range(len(start_coord)-i):
            print(removed)
            if abs(start_coord[i-removed][0]-start_coord[i+j-removed][0])<50 and \
               abs(start_coord[i-removed][1]-start_coord[i+j-removed][1])<50 and \
               abs(end_coord[i-removed][0]-end_coord[i+j-removed][0])<50 and \
               abs(end_coord[i-removed][1]-end_coord[i+j-removed][1])<50:
                print(start_coord[i-removed],start_coord[i+j-removed])
                start_coord.remove(start_coord[i+j-removed])
                end_coord.remove(end_coord[i+j-removed])
                removed += 1

    for i in range(len(start_coord)):
        cv2.line(img, start_coord[i],end_coord[i],(0,0,255),2)

    orb = cv2.ORB()

    # find the keypoints with ORB
    kp = orb.detect(img,None)

    # compute the descriptors with ORB
    kp, des = orb.compute(img, kp)

    img2 = cv2.drawKeypoints(img,kp,color=(0,255,0), flags=0)
    cv2.namedWindow("Corner")
    cv2.imshow("Corner",img2)

    cv2.namedWindow("Lines")
    cv2.imshow("Lines",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Ingen bild")
