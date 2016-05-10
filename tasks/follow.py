
import sys, os
sys.path.insert(0, os.path.abspath(".."))
import cv2
import numpy as np
from arduino.arduino import Arduino
from vision.button_detector import ButtonDetector
from config import capture_device, mega_usb
from vision.distance import DistanceCalculator
from time import sleep, time

def main():
    cap = cv2.VideoCapture(capture_device)
    #cap.set(cv2.cv.CV_CAP_PROP_FPS, 10)
    sleep(3) # let camera exposure settle

    hsv_range = np.array([[
        [130, 80, 100],
        [255, 255, 255]
    ], [
        [0, 80, 100],
        [30, 255, 255]
    ]])

    kalman = cv2.cv.CreateKalman(4, 2, 0)

    kalman.transition_matrix[0, 0] = 1
    kalman.transition_matrix[1, 1] = 1
    kalman.transition_matrix[2, 2] = 1
    kalman.transition_matrix[3, 3] = 1
    kalman.transition_matrix[0, 2] = 1
    kalman.transition_matrix[1, 3] = 1

    kalman.state_pre[0, 0] = 0
    kalman.state_pre[1, 0] = 0
    kalman.state_pre[2, 0] = 0
    kalman.state_pre[3, 0] = 0

    cv2.cv.SetIdentity(kalman.measurement_matrix, cv2.cv.RealScalar(1))
    cv2.cv.SetIdentity(kalman.process_noise_cov, cv2.cv.RealScalar(1e-5)) # 1e-5
    cv2.cv.SetIdentity(kalman.measurement_noise_cov, cv2.cv.RealScalar(1e-1))
    cv2.cv.SetIdentity(kalman.error_cov_post, cv2.cv.RealScalar(0.1))

    prediction = cv2.cv.KalmanPredict(kalman)
    print(prediction[0, 0], prediction[1, 0])

    button_detector = ButtonDetector(hsv_range)
    mega = Arduino(mega_usb)
    sleep(1) # init usb
    distCalc = DistanceCalculator(distance_mm=250., size_px=207.)

    scale = 1.0
    counter = 0
    minspeed = 8
    far_away_ts = time()

    while True:

        counter += 1

        # Input
        keyboard = cv2.waitKey(1) & 0xFF

        ret, frame = cap.read()

        small = cv2.resize(frame, (0, 0), fx=scale, fy=scale)

        ellipse = button_detector.find_button(small)

        if ellipse:
            print(ellipse)
            cv2.ellipse(small, ellipse, (0, 255, 0), 3)
            x = ellipse[0][0] - small.shape[1] / 2
            height = ellipse[1][1]
            correct = cv2.cv.CreateMat(2, 1, cv2.cv.CV_32FC1)
            correct[0, 0] = x
            correct[1, 0] = height
            cv2.cv.KalmanCorrect(kalman, correct)

        prediction = cv2.cv.KalmanPredict(kalman)
        #print(prediction[0, 0], prediction[1, 0])

        if prediction[1, 0]:
            distance = distCalc.convert(prediction[1, 0])
            x = prediction[0, 0]

            cv2.line(small, (small.shape[1] / 2, small.shape[0] / 2), (int((small.shape[1] / 2) + x), small.shape[0] / 2), (255, 0, 0), 3)

            distnorm = min(1, max(-1, (distance - 120) / 500))
            xnorm = min(1, max(-1, x / (small.shape[1] / 2)))

            rspeed = lspeed = max(distnorm * 20, minspeed)

            if rspeed != minspeed:
                far_away_ts = time()

            if time() - far_away_ts > 8:
                mega.send("light", True)
                break

            rspeed -= xnorm * 20
            lspeed += xnorm * 20

            if counter % 20 == 0:
                mega.send("lspeed", lspeed)
                mega.send("rspeed", rspeed)

        cv2.imshow('frame', small)

        if keyboard == ord('q'):
            break

    mega.send("lspeed", -10)
    mega.send("rspeed", -10)
    sleep(3)
    mega.send("lspeed", 0)
    mega.send("rspeed", 0)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
