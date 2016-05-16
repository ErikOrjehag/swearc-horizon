import zbar
import Image
import cv2

class DetectQRCode(object):

    @classmethod
    def detect_qr(self, image):

        # create a reader
        scanner = zbar.ImageScanner()

        # configure the reader
        scanner.parse_config('enable')

        # obtain image data
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY, dstCn=0)
        pil = Image.fromarray(gray)
        width, height = pil.size
        raw = pil.tostring()

        image = zbar.Image(width, height, 'Y800', raw)

        scanner.scan(image)

        for symbol in image:
            if symbol.data == "None":
                return None
            else:
                return symbol.data