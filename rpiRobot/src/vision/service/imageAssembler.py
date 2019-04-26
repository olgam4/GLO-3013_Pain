import io
from time import clock

import cv2
import numpy

from vision.domain.image import Image


class ImageAssembler:
    @staticmethod
    def to_string(image: Image) -> str:
        start_time = clock()
        image_content = image.content
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]
        result, encoded_image = cv2.imencode('.jpg', image_content, encode_param)
        with io.StringIO() as file_stream:
            numpy.savetxt(file_stream, encoded_image)
            image_text = file_stream.getvalue()
        return image_text
