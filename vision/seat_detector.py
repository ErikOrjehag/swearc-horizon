import cv2
import numpy as np


class SeatDetector():

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

    def seat_occupied(self, image):
        """
        TODO: Add docstring.
        :param image:
        :return:
        """

        # Create a mask used to find areas in the image that has
        # the same color as the seat occupant.
        color_mask = self.create_mask(image)

        # Only look in the centre
        height, width = image.shape[:2]
        centre_mask = np.zeros((height, width, 1), np.uint8)
        cv2.circle(centre_mask, (int(width / 2), int(height / 2)), int(height * 0.2), (255), -1)

        res_mask = cv2.bitwise_and(color_mask, centre_mask)

        # Cut out the parts of the image that has the correct color.
        res = cv2.bitwise_and(image, image, mask=res_mask)

        non_zero_centre_mask = cv2.countNonZero(centre_mask)
        non_zero_res_mask = cv2.countNonZero(res_mask)
        occupied = non_zero_res_mask > non_zero_centre_mask * 0.2

        # For debugging only.
        cv2.imshow("debug", res)
        #cv2.imshow("centre_mask", centre_mask)
        #cv2.imshow("color_mask", color_mask)

        return occupied

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
        hsv_image = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        mask = np.zeros(image.shape[:2], np.uint8)

        for hsv_range in self._hsv_range:
            hsv_lower = hsv_range[0]
            hsv_upper = hsv_range[1]

            # Create a mask (black and white) using the selected hsv range
            # tuned to find the button on the ticket machine.
            temp_mask = cv2.inRange(hsv_image, hsv_lower, hsv_upper)
            mask = cv2.bitwise_or(mask, temp_mask)

        # Kernel slides through the image. A pixel will be considered
        # white only if all pixels under the kernel are white.
        kernel = np.ones((10, 10), np.uint8)

        # Remove black junk inside objects.
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # Remove white junk outside objects.
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        return mask