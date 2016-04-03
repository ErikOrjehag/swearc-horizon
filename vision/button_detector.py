import cv2
import numpy as np
import math


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

        # Find the contours of the cut out parts.
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Find an ellipse that matches the contour that is most
        # probable to be the button on the ticket machine.
        ellipse = self.best_ellipse_in_contours(contours)

        # Using -1 means that we want to draw all contours.
        cv2.drawContours(res, contours, -1, (255, 255, 255), 1)

        if ellipse:
            cv2.ellipse(res, ellipse, (0, 255, 0), 3)

        # For debugging only.
        cv2.imshow("debug", res)

        return ellipse

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
        # TODO: Use multiple ranges (red hue wraps around)
        mask = cv2.inRange(hsv, hsv_lower, hsv_upper)

        # Kernel slides through the image. A pixel will be considered
        # white only if all pixels under the kernel are white.
        kernel = np.ones((10, 10), np.uint8)

        # Remove black junk inside objects.
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # Remove white junk outside objects.
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        return mask

    def best_ellipse_in_contours(self, contours):
        """
        Finds the contour that looks most like an ellipse.
        Works by fitting an ellipse around the contour and
        comparing the area. The ellipse with the least
        area difference is considered the best choice.

        :param contours: A list of contours.
        :return: An cv2 ellipse.
        """

        # TODO: Look slightly outside the button and look for the
        # TODO: correct color of the ticket machine.

        min_diff = None
        best_ellipse = None

        for contour in contours:

            # The function cv2.contourArea() requires at least 5 points.
            if len(contour) >= 5:

                ellipse = cv2.fitEllipse(contour)
                axis_a = ellipse[1][0] / 2
                axis_b = ellipse[1][1] / 2

                ellipse_area = math.pi * axis_a * axis_b
                contour_area = cv2.contourArea(contour)
                area_diff = abs(ellipse_area - contour_area)
                area_diff_dec = abs(1 - ellipse_area / contour_area)

                if area_diff_dec < 0.05:
                    if min_diff is None:
                        min_diff = area_diff
                        best_ellipse = ellipse
                    else:
                        if min_diff > area_diff:
                            min_diff = area_diff
                            best_ellipse = ellipse

        return best_ellipse

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
