import io

import cv2
import numpy

from vision.domain.image import Image


class ImageAssembler:
    @staticmethod
    def to_image(image_string: str) -> Image:
        with io.StringIO(image_string) as file_stream:
            encoded_image = numpy.loadtxt(file_stream, dtype='uint8')
        decoded_image = cv2.imdecode(encoded_image, cv2.IMREAD_COLOR)
        return Image(decoded_image)
