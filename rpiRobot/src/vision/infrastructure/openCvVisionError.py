from vision.domain.visionError import VisionError


class CameraDoesNotExistError(VisionError):
    """Exception raised when trying to create a camera with an invalid index"""

    def __init__(self, index: int) -> None:
        super().__init__('[OpenCV] Camera with id: {} doesnt exist'.format(index))


class AcquisitionError(VisionError):
    """Exception raised when an image could not be captured from a camera"""

    def __init__(self) -> None:
        super().__init__('[OpenCV] Error capturing image')


class CouldNotDetectQrCodeError(VisionError):
    """Exception raised when a Qr code could not be detected in an image"""

    def __init__(self) -> None:
        super().__init__('[OpenCV] Could not detect Qr code')


class CouldNotFindItemsError(VisionError):
    """Exception raised when no item could be detected in an image"""

    def __init__(self) -> None:
        super().__init__('[OpenCV] Could not find any items')


class CouldNotFindDestinationError(VisionError):
    """Exception raised when the destination could not be detected in an image"""

    def __init__(self) -> None:
        super().__init__('[OpenCV] Could not find destination')
