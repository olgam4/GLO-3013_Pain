from abc import ABC, abstractmethod

from vision.domain.image import Image


class IQrCodeReader(ABC):
    @abstractmethod
    def read_qr_code(self, image: Image) -> str:
        pass
