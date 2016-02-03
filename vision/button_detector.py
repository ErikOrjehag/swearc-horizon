import cv2
import numpy as np


class ButtonDetector():

    def __init__(self, hsv_range):
        """
        TODO: Add docstring.
        :param hsv_range:
        """
        # Instance variables.
        self._hsv_range = None

        # Initialization.
        self.set_hsv_range(hsv_range)

    def set_hsv_range(self, hsv_range):
        """
        TODO: Add docstring.
        :param hsv_range:
        """
        self._hsv_range = hsv_range.copy()

    def find_button(self, image):
        """
        TODO: Add docstring.
        :param image:
        :return:
        """

        # Create a mask used to find areas in the image that has
        # the same color as the button on the ticket machine.
        mask = self.create_mask(image)

        # Cut out the parts of the image that has the correct color.
        res = cv2.bitwise_and(image, image, mask=mask)

        # TODO: Add comment.
        # contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # TODO: Add comment.
        # self.find_circles(contours, res)

        # TODO: Add comment.

        circles = self.find_circles2(res)

        # Test show found circles.
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                # draw the outer circle
                cv2.circle(res, (i[0], i[1]), i[2], (0, 255, 0), 2)
                # draw the center of the circle
                cv2.circle(res, (i[0], i[1]), 2, (0, 255, 0), 2)

        # Using -1 means that we want to draw all contours.
        # cv2.drawContours(res, contours, -1, (255, 255, 255), 1)

        return res

    def create_mask(self, image):
        """
        TODO: Add docstring.
        :param image:
        :return:
        """
        # Blur to reduce details that produce noise.
        # Must be an odd number.
        blurred = cv2.medianBlur(image, 5)

        # Convert image from BGR to HSV because it's easier to work
        # with when we want to find the color of the button.
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        hsv_lower = self._hsv_range[0]
        hsv_upper = self._hsv_range[1]

        # Create a mask (black and white) using the selected hsv range
        # tuned to find the button on the ticket machine.
        mask = cv2.inRange(hsv, hsv_lower, hsv_upper)

        # Kernel slides through the image. A pixel will be considered
        # white only if all pixels under the kernel are white.
        kernel = np.ones((10, 10), np.uint8)

        # Remove black junk inside objects.
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # Remove white junk outside objects.
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        return mask

    def find_circles2(self, image):
        """
        TODO: Add docstring.
        :param image:
        :return:
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 1, 50, param1=20, param2=25, minRadius=10, maxRadius=0)
        return circles

    def find_circles(self, cnt1, res):
        acc = 3
        odia = 0
        for cnt in cnt1:
            count = 0
            old_dis = 0
            for pnt in cnt[0:(len(cnt) / 4)]:
                a = tuple(pnt[0])
                b = tuple(cnt[(len(cnt) / 2) + count][0])
                c = tuple(cnt[(len(cnt) / 4) + count][0])
                d = tuple(cnt[(len(cnt) / 2) + (len(cnt) / 4) + count][0])
                cv2.line(res, a, b, (255, 0, 0))
                dxa = a[0] - b[0]
                dya = a[1] - b[1]
                disa = np.sqrt((dxa * dxa + dya * dya))
                dxb = c[0] - d[0]
                dyb = c[1] - d[1]
                disb = np.sqrt((dxb * dxb + dyb * dyb))
                area = cv2.contourArea(cnt)
                dia = np.sqrt(4 * area / np.pi)
                leftmost = tuple(cnt[cnt[:, :, 0].argmin()][0])
                rightmost = tuple(cnt[cnt[:, :, 0].argmax()][0])
                topmost = tuple(cnt[cnt[:, :, 1].argmin()][0])
                bottommost = tuple(cnt[cnt[:, :, 1].argmax()][0])
                dxttb = topmost[0] - bottommost[0]
                dyttb = topmost[1] - bottommost[1]
                disttb = np.sqrt((dxttb * dxttb + dyttb * dyttb))
                dxltr = leftmost[0] - rightmost[0]
                dyltr = leftmost[1] - rightmost[1]
                disltr = np.sqrt((dxltr * dxltr + dyltr * dyltr))
                if disb - acc < disa < disb + acc and dia - acc <= disa <= dia + acc and disltr - acc <= disttb <= disltr + acc:
                    x, y, w, h = cv2.boundingRect(cnt)
                    cv2.rectangle(res, (x, y), (x + w, y + h), [0, 255, 255], 1)
                count += 1
                odia = dia