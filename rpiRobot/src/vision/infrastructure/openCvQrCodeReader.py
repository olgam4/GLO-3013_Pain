import cv2
import numpy as np

from vision.domain.image import Image
from vision.domain.iQrCodeReader import IQrCodeReader
from vision.infrastructure.openCvVisionError import CouldNotDetectQrCodeError


class OpenCvQrCodeReader(IQrCodeReader):
    def __init__(self) -> None:
        self._code = ''
        self._qr_decoder = cv2.QRCodeDetector()

    def read_qr_code(self, image: Image) -> str:
        image.process(self._process)
        return self._code

    def _process(self, image: np.ndarray) -> None:
        code, _, _ = self._qr_decoder.detectAndDecode(image)
        if len(code) > 0:
            self._code = code
        else:
            raise CouldNotDetectQrCodeError
